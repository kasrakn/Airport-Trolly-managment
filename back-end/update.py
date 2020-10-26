import threading
from trolleyApp.models import Trolly
from point_generator import trolley_positions
from datetime import datetime

def update_database():
    threading.Timer(10.0, update_database).start()
    print(trolley_positions)
    for i in trolley_positions.keys():
        coordinates = trolley_positions[i]
        x = float(coordinates[0])
        y = float(coordinates[1])
        if Trolly.objects.filter(trolley_id=int(i)).count() != 0:
            trolly_obj = Trolly.objects.get(trolley_id=int(i))
            trolly_obj.x = x
            trolly_obj.y = y
            trolly_obj.save()
        else:
            trolly_obj = Trolly(x=float(x), y=float(y), trolley_id=int(i), last_update=datetime.now())
            trolly_obj.save()
