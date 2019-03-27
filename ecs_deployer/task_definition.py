def create_task_definition(execution_role, memory, cpu):
    task_definition = {
        "networkMode": "awsvpc",
        "containerDefinitions": [],
        "executionRoleArn": execution_role,
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "memory": str(memory),
        "cpu": str(cpu)
    }

    return task_definition


def create_container_definition(env_vars, environment, project_name, container_name, ecr_path, command, cpu=256,
                                memory=512, ports=None):
    container_definition_name = "{}-{}".format(environment, project_name)
    log_path = "/ecs/{}-{}-{}".format(environment, project_name, container_name)

    port_mappings = []

    if ports:
        for p in ports:
            host_port = int(p.split(':')[0])
            container_port = int(p.split(':')[1])

            port_mappings.append({
                "hostPort": host_port,
                "protocol": "tcp",
                "containerPort": container_port
            })

    container_definition = {
        "environment": env_vars,
        "name": container_definition_name,
        "mountPoints": [],
        "image": ecr_path,
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-stream-prefix": "ecs",
                "awslogs-group": log_path,
                "awslogs-region": "eu-west-1"
            }
        },
        "cpu": cpu,
        "memory": memory,
        "portMappings": port_mappings,
        "command": parse_command(command),
        "essential": True,
        "volumesFrom": []
    }

    return container_definition


def parse_command(cmd):
    return cmd.split(' ')
