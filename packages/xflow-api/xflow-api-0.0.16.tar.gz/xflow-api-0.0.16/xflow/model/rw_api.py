from typing import Any

import ray

from structures import ModelSignature, ModelTypes
from xflow._utils.decorators import server_method
from xflow._private._constants import Actors


@server_method
def export_model(model_name: str, model_type: str, model_object: Any,
                 model_input: ModelSignature, model_output: ModelSignature):
    if model_type not in list(ModelTypes().__dict__.values()):
        raise ValueError(f"unsupported model type {model_type}. use ModelTypes class in xflow.model")
    if not isinstance(model_input, ModelSignature):
        raise ValueError(f"unsupported model signature {model_input} . use ModelSignature class in xflow.model")
    if not isinstance(model_output, ModelSignature):
        raise ValueError(f"unsupported model signature {model_output} . use ModelSignature class in xflow.model")
    if model_type == ModelTypes.TensorFlow:
        pass
    else:
        raise RuntimeError(f"model not supported. available: {ModelTypes.TensorFlow}")
    try:
        actor_id = ray.get_runtime_context().get_actor_id()
        manager_actor = ray.get_actor(Actors.MANAGER)
        owner_actor = ray.get(manager_actor.get_pool_actor_owner.remote(actor_id))
        owner_actor = ray.get_actor(owner_actor)
        pipeline, rev, trial = ray.get(owner_actor.get_pipeline_info.remote())
        xflow_worker_actor = ray.get_actor(Actors.XFLOW_WORKER)
    except Exception as exc:
        raise RuntimeError(f"can't get pipeline runtime context. {exc.__str__()}")
    try:
        ref = ray.put(model_object)
        ray.get(xflow_worker_actor.export_model.remote(pipeline=pipeline, revision=rev, trial=trial, model_name=model_name,
                                                       model_type=model_type, model_input=model_input,
                                                       model_output=model_output, model_object=ref))
        del ref
    except Exception as exc:
        raise RuntimeError(f"failed to export model. {exc.__str__()}")
    print(f"export model: {model_name} success")
