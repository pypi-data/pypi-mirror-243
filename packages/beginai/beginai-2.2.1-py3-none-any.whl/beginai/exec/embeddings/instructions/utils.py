def sequence_encoder(categories_list):
    """
    get a numerical code for each category.
    """
    categories_list = sorted(categories_list)
    return list(range(1, len(categories_list) + 1))


def sort_instructions(data) -> dict:
    if len(data) == 0:
        return {}

    def __sort_instructions(objects, template):
        sorted_dictionary = {}
        for object_key, object_instructions in objects.items():
            sorted_dictionary[object_key] = []

            # Check if it has an entry in the embedding template
            if object_key in template:
                # Loop through the embedding template entries
                for object_instruction_key in template[object_key]:
                    # Extract chained as a single instruction
                    if object_instruction_key.startswith("chain_instruction"):
                        object_instruction_key = object_instruction_key.split("__")[
                            3]

                        instruction = list(
                            filter(lambda x: x["f_id"] == object_instruction_key and x.get("_chains"), object_instructions))[0]
                    else:
                        instruction = list(filter(lambda x: x["f_id"] == object_instruction_key and not x.get(
                            "_chains", None), object_instructions))[0]

                    if instruction not in sorted_dictionary[object_key]:
                        sorted_dictionary[object_key].append(
                            instruction)
        return sorted_dictionary

    def __retrieve_actions_without_embedding(actions, template):
        actions_without_embedding = []
        template_keys = template.keys()
        
        for action in actions:
            if action not in template_keys:
                actions_without_embedding.append(action)
        return actions_without_embedding

    instructions = data.get("instructions", {})
    objects = instructions.get("objects", {})
    interactions = instructions.get("interactions", {})

    embedding_template = data.get("embedding_template", {})
    object_template = embedding_template.get("objects", {})
    interactions_template = embedding_template.get("interactions", {})

    sorted_dictionary = __sort_instructions(objects, object_template)

    if len(interactions):
        sorted_dictionary["interactions"] = {}

        for interaction_key in interactions:
            
            # For each object, there are two options:
            # 1) Have embedding associated with the action
            # 2) Just have the action name

            if interaction_key in interactions_template:
                template_for_key = interactions_template[interaction_key]
                sorted_dictionary["interactions"][interaction_key] = {
                    "with_embedding": __sort_instructions(interactions[interaction_key]["instructions"], template_for_key),
                    "just_actions": __retrieve_actions_without_embedding(interactions[interaction_key]['actions'], template_for_key)
                }
            else:
                sorted_dictionary["interactions"][interaction_key] = {
                    "with_embedding": {},
                    "just_actions": interactions[interaction_key]['actions']
                }
    return sorted_dictionary
