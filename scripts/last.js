cursor = db.weather.find().sort( { _id : -1 } ).limit(1);

while(cursor.hasNext()){
    printjson(cursor.next());
}
