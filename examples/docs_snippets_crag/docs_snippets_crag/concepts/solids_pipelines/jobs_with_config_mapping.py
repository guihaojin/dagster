from dagster import config_mapping, graph, op


@op(config_schema={"config_param": str})
def do_something(context):
    context.log.info("config_param: " + context.op_config["config_param"])


@graph
def do_it_all():
    do_something()


@config_mapping(config_schema={"simplified_param": str})
def simplified_config(val):
    return {"graph": {"do_something": {"config": {"config_param": val["simplified_param"]}}}}


do_it_all_with_simplified_config = do_it_all.to_job(config=simplified_config)

if __name__ == "__main__":
    # Will log "config_param: stuff"
    do_it_all_with_simplified_config.execute_in_process(run_config={"simplified_param": "stuff"})
