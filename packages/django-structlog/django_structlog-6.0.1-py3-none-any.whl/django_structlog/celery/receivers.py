import structlog

from . import signals


logger = structlog.getLogger(__name__)


def receiver_before_task_publish(sender=None, headers=None, body=None, **kwargs):
    context = structlog.contextvars.get_merged_contextvars(logger)
    if "task_id" in context:
        context["parent_task_id"] = context.pop("task_id")

    signals.modify_context_before_task_publish.send(
        sender=receiver_before_task_publish, context=context
    )

    import celery

    if celery.VERSION > (4,):
        headers["__django_structlog__"] = context
    else:
        body["__django_structlog__"] = context


def receiver_after_task_publish(sender=None, headers=None, body=None, **kwargs):
    logger.info(
        "task_enqueued",
        child_task_id=headers.get("id") if headers else body.get("id"),
        child_task_name=headers.get("task") if headers else body.get("task"),
    )


def receiver_task_pre_run(task_id, task, *args, **kwargs):
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(task_id=task_id)
    metadata = getattr(task.request, "__django_structlog__", {})
    structlog.contextvars.bind_contextvars(**metadata)
    signals.bind_extra_task_metadata.send(
        sender=receiver_task_pre_run, task=task, logger=logger
    )
    logger.info("task_started", task=task.name)


def receiver_task_retry(request=None, reason=None, einfo=None, **kwargs):
    logger.warning("task_retrying", reason=reason)


def receiver_task_success(result=None, **kwargs):
    signals.pre_task_succeeded.send(
        sender=receiver_task_success, logger=logger, result=result
    )
    logger.info("task_succeeded")


def receiver_task_failure(
    task_id=None,
    exception=None,
    traceback=None,
    einfo=None,
    sender=None,
    *args,
    **kwargs,
):
    throws = getattr(sender, "throws", ())
    if isinstance(exception, throws):
        logger.info(
            "task_failed",
            error=str(exception),
        )
    else:
        logger.exception(
            "task_failed",
            error=str(exception),
            exception=exception,
        )


def receiver_task_revoked(
    request=None, terminated=None, signum=None, expired=None, **kwargs
):
    metadata = getattr(request, "__django_structlog__", {}).copy()
    metadata["task_id"] = request.id
    metadata["task"] = request.task

    logger.warning(
        "task_revoked",
        terminated=terminated,
        signum=signum.value if signum is not None else None,
        signame=signum.name if signum is not None else None,
        expired=expired,
        **metadata,
    )


def receiver_task_unknown(message=None, exc=None, name=None, id=None, **kwargs):
    logger.error(
        "task_not_found",
        task=name,
        task_id=id,
    )


def receiver_task_rejected(message=None, exc=None, **kwargs):
    logger.exception("task_rejected", task_id=message.properties.get("correlation_id"))


def connect_celery_signals():
    from celery.signals import before_task_publish, after_task_publish

    before_task_publish.connect(receiver_before_task_publish)
    after_task_publish.connect(receiver_after_task_publish)
