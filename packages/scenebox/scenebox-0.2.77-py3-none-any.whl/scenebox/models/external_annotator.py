from typing import Optional, List, Any, Dict
from abc import abstractmethod

from ..clients import SceneEngineClient
from ..constants import AssetsConstants, JobConstants, AnnotationGroups, AnnotationTypes
from ..custom_exceptions import OperationError
from ..tools.logger import get_logger
from .operations import BaseOperation
from .annotation import Annotation, BoundingBoxAnnotation, PolygonAnnotation, PointAnnotation, LineAnnotation, \
    SegmentationAnnotation
from ..tools.misc import get_md5_from_string

logger = get_logger(__name__)


class ExternalAnnotator(BaseOperation):
    """Base annotation class. Inherited by all annotator classes."""

    # SceneBox authentication (for SceneEngineClient, AssetManagerClient, etc.)
    def __init__(self,
                 scene_engine_client: SceneEngineClient):
        super().__init__(scene_engine_client=scene_engine_client)

        # All connections to external annotators need the following scenebox data:
        self.sets_amc = self.sec.get_asset_manager(AssetsConstants.SETS_ASSET_ID)
        self.images_amc = self.sec.get_asset_manager(AssetsConstants.IMAGES_ASSET_ID)
        self.annotations_amc = self.sec.get_asset_manager(AssetsConstants.ANNOTATIONS_ASSET_ID)

        self.annotator_name = None
        self.config_schema = None
        self.input_schema = None
        self.output_schema = None
        self.phase_params_schema = None

    def process(self,
                instance_id: str,
                job_id: str,
                input_payload: dict,
                config: Optional[dict] = None,
                phase: Optional[str] = None,
                phase_payload: Optional[dict] = None):

        logger.info("TASK - annotation with {} STARTED".format(self.annotator_name))

        job = self.sec.get_job_manager(job_id=job_id)
        job.run()

        if config:
            self._validate_config(config=config)
        else:
            raise OperationError("Config for operation {} is empty".format(instance_id))

        if input_payload:
            self._validate_input_payload(input_payload=input_payload)
        else:
            raise OperationError("Input payload for operation {} is empty".format(instance_id))

        if phase_payload:
            self._validate_phase_params(phase_name=phase, phase_params=phase_payload)

        input_set_ids = input_payload.get("sets")
        all_phases_completed = False
        output_payload = {
            "sets": []
        }

        if phase == "send_data":
            logger.info("Phase: Send Data")
            self.send_data_to_annotator(operation_instance_id=instance_id,
                                        job_id=job_id,
                                        input_set_ids=input_set_ids,
                                        config=config,
                                        send_data_payload=phase_payload)

            # Save current phase in operation state
            self.save_state(instance_id=instance_id, state_dict={"current_phase": "send_data"})

            job.finish()
            logger.info("TASK - {}: Sets {} sent:::".format(self.annotator_name, input_set_ids))

        elif phase == "receive_annotations":
            logger.info("Phase: Receive Annotations")
            previous_phase = self.get_state(instance_id=instance_id).get("current_phase")
            if previous_phase in ["send_data", "receive_annotations"]:
                output_set_ids = self.receive_annotations_from_annotator(
                    operation_instance_id=instance_id,
                    job_id=job_id,
                    config=config,
                    input_set_ids=input_set_ids,
                    receive_annotations_payload=phase_payload)

                # Build output payload
                output_payload = {
                    "sets": output_set_ids
                }
                # Save current phase in operation state
                self.save_state(instance_id=instance_id, state_dict={"current_phase": "receive_annotations"})
                all_phases_completed = True

                job.finish()
                logger.info("TASK - {}: Annotations for sets {} received:::".format(self.annotator_name,
                                                                                    input_set_ids))
            else:
                job.abort()
                raise OperationError("Send data phase not executed. Nothing to receive.")

        return output_payload, all_phases_completed

    def create_output_annotation_sets(self,
                                      operation_instance_id: str,
                                      input_set_ids: List[str]) -> dict:
        """
        Creates a set to collect the annotations for each input set and returns a map
        of {input_set: output_set}
        """

        input_output_set_map = {}
        input_set_id_to_meta = self.sets_amc.get_metadata_in_batch(ids=input_set_ids,
                                                                   source_selected_fields=["id", "name"])

        for input_set_id, input_set_meta in input_set_id_to_meta.items():
            output_set_name = f"{input_set_id}_{operation_instance_id}"
            output_set_id = get_md5_from_string(output_set_name)

            if not self.sets_amc.exists(id=output_set_id):
                output_set_id = self.sec.create_set(name=output_set_name,
                                                    id=output_set_id,
                                                    asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID,
                                                    origin_set_id=input_set_id)
            input_output_set_map[input_set_id] = output_set_id

        return input_output_set_map

    @abstractmethod
    def send_images_to_annotator(self,
                                 operation_instance_id: str,
                                 input_set_ids: List[str],
                                 config: Dict[str, Any],
                                 send_images_payload: Dict[str, Any],
                                 job_id: str,
                                 **kwargs):
        raise NotImplementedError(f"Sending images to {self.annotator_name} has not yet been implemented.")

    @abstractmethod
    def receive_image_annotations(self,
                                  operation_instance_id: str,
                                  input_output_sets_map: dict,
                                  receive_annotations_payload: Dict[str, Any],
                                  config: Dict[str, Any],
                                  job_id: str,
                                  **kwargs):
        raise NotImplementedError(f"Receiving images from {self.annotator_name} has not yet been implemented.")

    def drop_unmodified_image_annotations(self,
                                          image_id_to_annotations: Dict[str, List[Annotation]]) -> \
            (Dict[str, List[Annotation]], List[str]):
        return image_id_to_annotations, []

    def send_data_to_annotator(self,
                               operation_instance_id: str,
                               job_id: str,
                               input_set_ids: List[str],
                               config: dict,
                               send_data_payload: dict):

        job = self.sec.get_job_manager(job_id=job_id)
        if job.get_status() != JobConstants.STATUS_RUNNING:
            job.run()

        self.send_images_to_annotator(operation_instance_id=operation_instance_id,
                                      input_set_ids=input_set_ids,
                                      job_id=job_id,
                                      config=config,
                                      send_images_payload=send_data_payload)

    def receive_annotations_from_annotator(self,
                                           operation_instance_id: str,
                                           job_id: str,
                                           config: dict,
                                           input_set_ids: List[str],
                                           receive_annotations_payload: dict):
        media_types = []
        input_output_sets_map = self.create_output_annotation_sets(input_set_ids=input_set_ids,
                                                                   operation_instance_id=operation_instance_id)
        job = self.sec.get_job_manager(job_id=job_id)

        for input_set_id in input_set_ids:
            set_metadata = self.sets_amc.get_metadata(input_set_id)
            media_types = set_metadata.get("assets_type")

        if AssetsConstants.IMAGES_ASSET_ID in media_types:
            image_id_to_annotations = \
                self.receive_image_annotations(operation_instance_id=operation_instance_id,
                                               job_id=job_id,
                                               config=config,
                                               input_output_sets_map=input_output_sets_map,
                                               receive_annotations_payload=receive_annotations_payload)

            annotations = self.update_image_annotations(input_output_sets_map=input_output_sets_map,
                                                        image_id_to_annotations=image_id_to_annotations,
                                                        receive_annotations_payload=receive_annotations_payload,
                                                        job_id=job_id,
                                                        config=config)

            # get all mask annotation ids
            mask_annotation_ids = [annotation.id for annotation in annotations if
                                   annotation.annotation_type == AnnotationTypes.SEGMENTATION]
            if mask_annotation_ids:
                job.update_stage("Cleaning masks")
                self.sec.cleanup_annotation_masks(ids=mask_annotation_ids,
                                                  wait_for_completion=True)

        elif any([AssetsConstants.IMAGES_ASSET_ID != media_type for media_type in media_types]):
            raise NotImplementedError(f"Media types other than images are not supported for receive."
                                      f"Given media types: {media_types}")

        return list(input_output_sets_map.values())

    def _delete_old_annotations(self,
                                input_output_sets_map: dict,
                                **kwargs):
        output_set_names = list(input_output_sets_map.values())
        annotations_query = {"filters": [{"field": "sets",
                                          "values": output_set_names,
                                          "filter_out": False}]}
        self.sec.delete_annotations(search=annotations_query)

        return

    def update_lidar_annotations(self):
        raise NotImplementedError()

    def update_video_annotations(self):
        raise NotImplementedError()

    def clean_images_and_annotations(self,
                                     input_output_sets_map: dict,
                                     image_id_to_annotations: Dict[str, List[Annotation]]):
        clean_asset_id_to_scenebox_annotations, dropped_annotation_ids = \
            self.drop_unmodified_image_annotations(image_id_to_annotations=image_id_to_annotations)
        self._delete_old_annotations(input_output_sets_map=input_output_sets_map,
                                     image_id_to_annotations=image_id_to_annotations,
                                     dropped_annotation_ids=dropped_annotation_ids)

        return clean_asset_id_to_scenebox_annotations

    @staticmethod
    def create_empty_annotation(
            default_type: str,
            asset_id: str,
            media_type: str,
            provider: str,
            version: str,
            output_set_id: str) -> Annotation:

        kwargs = {"id": f"{provider}_{asset_id}_{default_type}",
                  "asset_id": asset_id,
                  "media_type": media_type,
                  "provider": provider,
                  "annotation_group": AnnotationGroups.GROUND_TRUTH,
                  "set_id": output_set_id,
                  "version": version}

        if default_type == AnnotationTypes.TWO_D_BOUNDING_BOX:
            return BoundingBoxAnnotation(bounding_boxes=[], **kwargs)
        elif default_type == AnnotationTypes.POLYGON:
            return PolygonAnnotation(polygons=[], **kwargs)
        elif default_type == AnnotationTypes.POINT:
            return PointAnnotation(points=[], **kwargs)
        elif default_type == AnnotationTypes.LINE:
            return LineAnnotation(lines=[], **kwargs)
        elif default_type == AnnotationTypes.SEGMENTATION:
            return SegmentationAnnotation(labels=[],
                                          mask_colors=[],
                                          mask_urls=[],
                                          **kwargs)
        else:
            raise TypeError(f"Default annotation type {default_type} not recognized.")

    def append_default_annotations(self,
                                   image_id_to_annotations: Dict[str, List[Annotation]],
                                   default_type: str,
                                   provider: str,
                                   media_type: str,
                                   version: str,
                                   input_output_sets_map: dict) -> Dict[str, List[Annotation]]:

        image_ids = list(image_id_to_annotations.keys())
        input_set_ids = list(input_output_sets_map.keys())
        input_set_id_to_metadata = self.sets_amc.get_metadata_in_batch(ids=input_set_ids)
        image_id_to_metadata = self.images_amc.get_metadata_in_batch(ids=image_ids,
                                                                     source_selected_fields=["id", "annotations",
                                                                                             "annotations_meta",
                                                                                             "sets"])
        for image_id, annotations in image_id_to_annotations.items():

            if not annotations:
                if media_type == AssetsConstants.IMAGES_ASSET_ID:
                    sets_meta = image_id_to_metadata[image_id].get("sets")
                else:
                    raise NotImplementedError()

                # Lazy matching: assume there is only one match between input sets and the current asset
                input_set_id = input_set_ids[0]  # Default in case no match is found
                output_set_id = input_output_sets_map[input_set_id]
                for input_set_id, input_set_metadata in input_set_id_to_metadata.items():
                    input_set_name = input_set_metadata.get("name")
                    if any([set_ == input_set_name for set_ in sets_meta]):
                        break

                default_annotation = self.create_empty_annotation(
                    asset_id=image_id,
                    default_type=default_type,
                    media_type=media_type,
                    provider=provider,
                    version=version,
                    output_set_id=output_set_id)

                if default_annotation.id not in image_id_to_metadata.get("annotations", []):
                    image_id_to_annotations[image_id].append(default_annotation)

        return image_id_to_annotations

    def update_image_annotations(self,
                                 input_output_sets_map: dict,
                                 receive_annotations_payload: dict,
                                 image_id_to_annotations: Dict[str, List[Annotation]],
                                 job_id: str,
                                 config: dict,
                                 add_default_annotations: bool = True):

        provider = receive_annotations_payload.get("annotation_provider", self.annotator_name)
        default_type = config.get("annotation_type")
        version = receive_annotations_payload.get("annotation_version")

        job = self.sec.get_job_manager(job_id=job_id)

        job.update_stage("Preparing image metadata for new annotations")
        job_progress = job.get_progress()
        job.update_progress(progress=job_progress + 0.8 * (90 - job_progress))
        image_id_to_annotations = self.clean_images_and_annotations(input_output_sets_map=input_output_sets_map,
                                                                    image_id_to_annotations=image_id_to_annotations)

        if add_default_annotations:
            job.update_stage("Appending default annotations")
            job_progress = job.get_progress()
            job.update_progress(progress=job_progress + 0.9 * (90 - job_progress))
            image_id_to_annotations = self.append_default_annotations(image_id_to_annotations=image_id_to_annotations,
                                                                      default_type=default_type,
                                                                      provider=provider,
                                                                      version=version,
                                                                      media_type=AssetsConstants.IMAGES_ASSET_ID,
                                                                      input_output_sets_map=input_output_sets_map)

        job.update_stage("Uploading annotations into SceneBox")
        job_progress = job.get_progress()
        job.update_progress(progress=job_progress + 0.95 * (100 - job_progress))
        annotations = [annotation for annotation_list in image_id_to_annotations.values()
                       for annotation in annotation_list if annotation]
        self.sec.add_annotations(annotations=annotations,
                                 annotations_to_objects=True)

        return annotations
