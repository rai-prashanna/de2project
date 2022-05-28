db = db.getSiblingDB("q1");
db.lang.drop();

db.lang.insertMany([
    {
        "id": 1,
        "python": "100",
        "java": "111",
	"c": "10"
    },
    {
        "id": 2,
        "python": "2",
        "jave": "1",
	"c": "56"
    },
]);
