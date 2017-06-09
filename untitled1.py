from flask import Flask
from flask import render_template
from flask import request
import time

app = Flask(__name__)


@app.route('/')
def Home():
    from DbClass import DbClass
    db = DbClass()
    food_eaten = db.getFood_eaten()
    food_size=0
    for value in food_eaten:
        if value[1] =='kg':
            weight = float(value[0] *1000)
        else:
            weight=float(value[0])
        food_size=weight+food_size
        print(food_size)

    if food_size > 1000:
        food_size=float(food_size/1000)
        food_eaten = [food_size,'kg']
    else:
        food_eaten = [food_size, 'g']

    naam= db.getDog_info()
    naam=naam[-1]
    print(naam)

    food_reservoir = db.getFood_reservoir()
    print(food_reservoir)
    food_reservoir = food_reservoir[-1]
    print(food_reservoir)

    return render_template('index.html',eaten=food_eaten,naam=naam, reservoir = food_reservoir)

@app.route('/manualFeed' ,methods=['GET','POST'])
def manualFeed():
    from DbClass import DbClass
    from a4988 import a4988
    from HX711 import HX711
    db = DbClass()
    mot=a4988()
    hx=HX711(21,20)


    naam= db.getDog_info()
    naam=naam[-1]

    food_reservoir = db.getFood_reservoir()
    food_reservoir = food_reservoir[-1]

    rest_portionsize = db.getResting_portionsize()
    rest_portionsize = rest_portionsize[-1]
    rest_portionsize=rest_portionsize[0]

    portion = request.form["portionsize"]
    unit = request.form["unit"]

    if unit=='g':
        turn=int(int(portion)/20)
    else:
        turn=int((int(portion)*1000)/20)
        portion = int(portion)*1000

    if int(portion) < int(rest_portionsize):

        hx.set_reading_format("LSB", "MSB")
        hx.set_reference_unit(2167)
        hx.reset()
        hx.tare()


        for i in range(0,turn):
            mot.turn_motor()

        list_weight=[]
        for i in range(0,10):
            val = max(0, int(hx.get_weight(5)))
            print(val)
            hx.power_down()
            hx.power_up()
            list_weight.append(int(val))
            time.sleep(0.5)


        weight=sorted(list_weight)
        portion_weight= int(weight[-1])

        if portion_weight > 1000 :
            portion_Data= float(portion_weight/1000)
            db.setDataToFood_eaten(portion_Data,2,0)
        else:
            db.setDataToFood_eaten(portion_weight,1,0)

        rest_portionsize = rest_portionsize - portion_weight
        print(rest_portionsize)

        if rest_portionsize < 0 :
            rest_portionsize = 0
        else:
            rest_portionsize = rest_portionsize

        db.setDataToResting_portionsize(rest_portionsize,1)

    food_eaten = db.getFood_eaten()
    food_size = 0
    for value in food_eaten:
        if value[1] == 'kg':
            weight = float(value[0] * 1000)
        else:
            weight = float(value[0])
        food_size = weight + food_size
        print(food_size)

    if food_size > 1000:
        food_size = float(food_size / 1000)
        food_eaten = [food_size, 'kg']
    else:
        food_eaten = [food_size, 'g']

    return render_template('index.html',eaten=food_eaten,naam=naam, reservoir = food_reservoir)

@app.route('/settings')
def Settings():
    from DbClass import DbClass
    db = DbClass()

    dog_info=db.getDog_info()
    dog_info=dog_info[-1]

    max_portionsize = db.getMax_portionsize()
    max_portionsize=max_portionsize[-1]
    cur_max_portionsize = max_portionsize[0]
    unit_max = max_portionsize[1]
    if unit_max==1:
        unit_max='g'
    else:
        unit_max='kg'

    weight=dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]
    return render_template('settings.html',recommended = portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize, unit_max=unit_max)




@app.route('/addInfo',methods=['GET','POST'])
def addData():
    from DbClass import DbClass
    db = DbClass()
    name=request.form["name"]
    weight = request.form["weight"]
    unit = request.form["unit"]
    if unit == 'kg':
        unit=2
    else:
        unit=1
    age= request.form["age"]
    birthday=request.form["birthday"]
    print(name)
    db.setDataToDog_info(name,weight,unit,age,birthday)

    dog_info = db.getDog_info()
    dog_info = dog_info[-1]

    max_portionsize = db.getMax_portionsize()
    max_portionsize = max_portionsize[-1]
    cur_max_portionsize=max_portionsize[0]
    unit_max = max_portionsize[1]
    if unit_max==1:
        unit_max='g'
    else:
        unit_max='kg'


    weight = dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]

    return render_template('settings.html',recommended=portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize,unit_max=unit_max)


@app.route('/time')
def feedTimes():
    from DbClass import DbClass
    db = DbClass()
    timelist = db.getFeedingTimes()
    timelist= sorted(timelist)

    return render_template('feeding_times.html',timelist=timelist)

@app.route('/time/newtime')
def newTimes():
    return render_template('add_time.html',)

@app.route('/addTime',methods=['GET','POST'])
def addTime():
    from DbClass import DbClass
    db = DbClass()
    time=request.form["time"]
    db.setDataToFeeding_times(time)
    return render_template('add_time.html')

@app.route('/addPortion',methods=['GET','POST'])
def addPortion():
    from DbClass import DbClass
    db = DbClass()
    portion = request.form["portion"]
    print(portion)
    unit = request.form["unit"]
    if unit == 'kg':
        unit=2
    else:
        unit=1
        print(float(portion))
    db.setDataToMax_portionSize(float(portion),int(unit))

    dog_info = db.getDog_info()
    dog_info = dog_info[-1]

    max_portionsize = db.getMax_portionsize()
    max_portionsize = max_portionsize[-1]
    cur_max_portionsize = max_portionsize[0]
    unit_max = max_portionsize[1]
    if unit_max==1:
        unit_max='g'
    else:
        unit_max='kg'

    weight = dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]

    return render_template('settings.html',recommended=portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize, unit=unit_max)

@app.route('/history')
def history():
    return render_template('history.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
