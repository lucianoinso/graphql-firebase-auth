db = db.getSiblingDB('mydb');

db.users.insertMany([
  { name: "Oreo", gender: "male", age: 2, interests: ["exploring shopping bags", "napping in the sun"], characteristics: ["curious", "dynamic"]},
  { name: "Lua", gender: "female", age: 3, interests: ["running after balls", "climbing curtains", "hunt toys"], characteristics: ["energetic", "playful", "alert"]},
  { name: "Astarion", gender: "male", age: 4, interests: ["looking outside the window", "hunting red dots"], characteristics: ["tranquil", "curious", "intelligent"]},
  { name: "Bellybutton", gender: "male", age: 5, interests: ["climb furnitures", "explore under the sofa", "nap inside boxes"], characteristics: ["adventurer", "curious", "cute"]}
]);
