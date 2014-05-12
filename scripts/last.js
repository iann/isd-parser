cursor = db.weather.find().sort( { _id : -6 } ).limit(1);

while(cursor.hasNext()){
    printjson(cursor.next());
}
