from datetime import date


location_data = [
    {'id': '1', 'name': 'Lagos', 'zone': "+1"},
    {'id': '2', 'name': 'Nairobi', 'zone': "+3"},
    {'id': '3', 'name': 'Kampala', 'zone': "+3"},
    {'id': '4', 'name': 'Kigali', 'zone': "+2"},
]
role_data = [
    {'id': '1', 'name': 'admin'},
    {'id': '2', 'name': 'user'},
]

user_data = [
    {'id': '1',
     'slack_id': '-L5J538y77WvOnzJ1FPG',
     'first_name': 'Eno',
     'last_name': 'Basey',
     'user_id': '-L5J538y77WvOnzJ1FPG',
     'user_type_id': '1'},
    {'id': '2',
     'slack_id': '-K_djydLXD3FE_w141iJ',
     'first_name': 'Ayo',
     'last_name': 'Ajebeku',
     'user_id': '-K_djydLXD3FE_w141iJ',
     'user_type_id': '2'}
]

user_role_data = [
    {'id': '1', 'role_id': '1', 'user_id': '-L5J538y77WvOnzJ1FPG', "email": "eno.bassey@andela.com"},
    {'id': '2', 'role_id': '1', 'user_id': '-K_djydLXD3FE_w141iJ', "email": "ayoola.ajebeku@andela.com"},
]

permission_data = [
    {'id': '1', 'name': 'view_meal_item', 'role_id': '1', 'keyword': 'view_meal_item'},
    {'id': '2', 'name': 'create_meal_item', 'role_id': '1', 'keyword': 'create_meal_item'},
    {'id': '3', 'name': 'update_meal_item', 'role_id': '1', 'keyword': 'update_meal_item'},
    {'id': '4', 'name': 'delete_meal_item', 'role_id': '1', 'keyword': 'delete_meal_item'},
    {'id': '5', 'name': 'create_menu', 'role_id': '1', 'keyword': 'create_menu'},
    {'id': '6', 'name': 'delete_menu', 'role_id': '1', 'keyword': 'delete_menu'},
    {'id': '7', 'name': 'view_menu', 'role_id': '1', 'keyword': 'view_menu'},
    {'id': '8', 'name': 'update_menu', 'role_id': '1', 'keyword': 'update_menu'},
    {'id': '9', 'name': 'view_orders', 'role_id': '1', 'keyword': 'view_orders'},
    {'id': '10', 'name': 'view_roles', 'role_id': '1', 'keyword': 'view_roles'},
    {'id': '11', 'name': 'create_roles', 'role_id': '1', 'keyword': 'create_roles'},
    {'id': '12', 'name': 'delete_roles', 'role_id': '1', 'keyword': 'delete_roles'},
    {'id': '13', 'name': 'view_user_roles', 'role_id': '1', 'keyword': 'view_user_roles'},
    {'id': '14', 'name': 'create_user_roles', 'role_id': '1', 'keyword': 'create_user_roles'},
    {'id': '15', 'name': 'delete_user_roles', 'role_id': '1', 'keyword': 'delete_user_roles'},
    {'id': '16', 'name': 'view_permissions', 'role_id': '1', 'keyword': 'view_permissions'},
    {'id': '17', 'name': 'create_permissions', 'role_id': '1', 'keyword': 'create_permissions'},
    {'id': '18', 'name': 'delete_permissions', 'role_id': '1', 'keyword': 'delete_permissions'},
    {'id': '19', 'name': 'delete_vendor', 'role_id': '1', 'keyword': 'delete_vendor'},
    {'id': '20', 'name': 'delete_engagement', 'role_id': '1', 'keyword': 'delete_engagement'},
    {'id': '21', 'name': 'view_ratings', 'role_id': '1', 'keyword': 'view_ratings'},
    {'id': '22', 'name': 'view_users', 'role_id': '1', 'keyword': 'view_users'},
    {'id': '23', 'name': 'delete_user', 'role_id': '1', 'keyword': 'delete_user'},
    {'id': '24', 'name': 'create_user', 'role_id': '1', 'keyword': 'create_user'},
    {'id': '25', 'name': 'update_user', 'role_id': '1', 'keyword': 'update_user'},
]

meal_items_data = [
    {'id': '1', 'name': 'Rice', 'meal_type': 'main', 'image': 'https://res.cloudinary.com/dunnio1id/image/upload/v1541563827/coipoqf9juupefah6zdd.jpg', 'location_id': '1'},
    {'id': '2', 'name': 'Fish', 'meal_type': 'protein', 'image': 'https://res.cloudinary.com/dunnio1id/image/upload/v1540382001/s9sjlcbiistxukpih3gn.jpg', 'location_id': '1'},
    {'id': '3', 'name': 'White boll', 'meal_type': 'side', 'image': 'https://res.cloudinary.com/abdulfatai/image/upload/v1543265435/vajcsugdpgnja0v7rid2.jpg', 'location_id': '1'},
]

vendor_data = [
    {'id': '1',
     'name': 'Vendor 1',
     'address': 'Vendor address',
     'tel': '+25671234567',
     'contact_person': 'Joseph',
     'is_active': True,
     'location_id': '1',
     'average_rating': '4.3'}
]

vendor_engagement_data = [
    {'id': '1',
     'vendor_id': '1',
     'location_id': '1',
     'start_date': date.today().strftime('%Y-%m-%d'),
     'end_date': date.today().strftime('%Y-%m-%d'),
     'status': '1',
     'termination_reason': None}
]

menu_data = [
    {'id': '1',
     'date': date.today().strftime('%Y-%m-%d'),
     'meal_period': 'lunch',
     'main_meal_id': '1',
     'allowed_side': '3',
     'allowed_protein': '2',
     'side_items': '1,2',
     'protein_items': '1,2',
     'vendor_engagement_id': '1',
     'location_id': '1'}
]

orders_data = [
    {'id': '1',
     'user_id': '-L5J538y77WvOnzJ1FPG',
     'date_booked_for': date.today().strftime('%Y-%m-%d'),
     'date_booked': date.today().strftime('%Y-%m-%d'),
     'channel': 'slack',
     'meal_period': 'lunch',
     'order_status': 'booked',
     'has_rated': False,
     'menu_id': '1',
     'location_id': '1'
     }
]

meal_item_orders_data = [
    {'order_id': '1', 'meal_item_id': '1'},
    {'order_id': '1', 'meal_item_id': '2'},
    {'order_id': '1', 'meal_item_id': '3'},
]
