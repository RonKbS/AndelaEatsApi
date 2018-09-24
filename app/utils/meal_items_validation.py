from app.utils.enums import MealTypes


def validate_meal_items(payload):
  """
    This method validates the Request payload
    for creating a group of meal items:
      mealType, name, description and imageUrl
  """

  response = dict(
    error = dict(
      message = None,
      statusCode = ''
    ),
    mealType = [],
  )

  for value in payload:
    if not value.get('name') or not value.get('name').strip(' '):
      response['error']['message'] = 'meal item name is required for all meal items'
      response['error']['statusCode'] = 400
      break

    if not value.get('description') or not value.get('description').strip(' '):
      response['error']['message'] = 'meal item description is required for all meal items'
      response['error']['statusCode'] = 400
      break

    if not value.get('imageUrl') or not value.get('imageUrl').strip(' '):
      response['error']['message'] = 'meal item imageUrl is required for all meal items'
      response['error']['statusCode'] = 400
      break

    try:
      mealType = MealTypes.has_value(value.get('mealType'))
    except Exception as error:
      error = 'Please confirm the mealType and try again'

    # if mealType is False:
    #   response['error']['message'] = 'mealType for ' +  value.get('name') + ' does not exist'
    #   response['error']['statusCode'] = 404
    #   break

    response['mealType'].append(value.get('mealType'))

  return response