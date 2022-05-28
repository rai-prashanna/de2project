db = db.getSiblingDB("animal_db");
db.animal_tb.drop();

db.animal_tb.insertMany([
    {
        "id": 1,
        "python": "100",
        "java": "50",
	"c": "10"
    },
]);
