from andelaeats.constants.success import messages


def delete_by_id(model, id, *success_message_args):
    model_instance = model.get_or_404(id)
    model_instance.delete()
    return {"msg": "OK", "payload": messages["deleted"].format(*success_message_args)}
