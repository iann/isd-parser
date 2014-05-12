db = db.getSiblingDB('weather');

cursor = db.weather.find({stationId: "725090-14739", year: 2013})

while(cursor.hasNext()){
    printjson(cursor.next());
}
