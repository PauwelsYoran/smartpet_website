from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def Home():
    from DbClass import DbClass
    db = DbClass()
    food_eaten = db.getFood_eaten()
    food_eaten= food_eaten[-1]

    naam= db.getDog_info()
    naam=naam[-1]
    print(naam)

    food_reservoir = db.getFood_reservoir()
    print(food_reservoir)
    food_reservoir = food_reservoir[-1]
    print(food_reservoir)

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
    unit = request.form["unit"]
    if unit == 'kg':
        unit=2
    else:
        unit=1
    db.setDataToMax_portionSize(int(portion),int(unit))

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
