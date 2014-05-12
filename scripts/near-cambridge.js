db = db.getSiblingDB('stations');

cursor = db.stations.find(
    {
        loc:
        { $near :
            {
                $geometry : { type : "Point" , coordinates: [ -71.11 , 42.37 ] },
                $maxDistance : 10000
            }
        }
    }
)

while(cursor.hasNext()){
    printjson(cursor.next());
}
