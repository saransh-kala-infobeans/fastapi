//variables, let const var
//let -> used normally. block-scoped. 
//const -> A const variable cannot be re-assigned, it CAN BE modified, but NOT RE-ASSIGNED.
//var -> OLD, function-scoped -- leaks outta conditional/loop blocks. Just don't use this.

let num1 = 1;

const num2 = 2;
//num2 = 3;  <== this is invalid

var num3 = 3;

const person = {
  name: "Alice"
};
person.name = "Bob"; // ✅ allowed, const only prevents reassignement, not mutability

const string = "Hello";
string.concat(" World");
console.log(string);


const add = (a, b) => a+b;
console.log(add(3,4));


//JS OBJECT VS JSON
//These may look VERY similar, as JSON literally stands from JavaScript Object Notation.

//object;
const js_object = {
  name : "Saransh",
  age : 20,
  isMarried : false,
  hobbies : ["Art", "Music"],
};

//to access the values inside the object you can either use the sq brackets as objectName["property_name"] 
//or the dot operator as objectName.property
console.log(js_object["name"]);  //OR
console.log(js_object.name, js_object.age)

//FOR-EACH LOOP
// for(const key in js_object){
//   console.log(key); //get all keys.
//   console.log(js_object[key]); //get all values.
// }

//modifying/adding into object.
js_object.email = "saransh.kala@infobeans.com";
console.log(js_object["email"]);

//delect key-value from object.
delete js_object.age; //removing age property from the object.
console.log(js_object);

// #JSON.parse() and JSON.stringify()

//convert JS object --> string (JSON as string)
const object_string = JSON.stringify(js_object);
console.log(object_string);
//you'll get something like : {"name":"Saransh","isMarried":false,"hobbies":["Art","Music"],"email":"saransh.kala@infobeans.com"}


//convert JSON string to JS object
const object = JSON.parse(object_string);
console.log(object);
console.log(object["email"]);

//just for information : 
//In Postman, instead of using JSON.parse(), we can use pm.response.json();


//ARRAYS, important methods.
const arr = [1,2,3,4,5];

//1. length
console.log(arr.length);

//2. indexOf
console.log(arr.indexOf(3));

//3. includes : returns a boolean.
console.log(arr.includes(5));

//4. push(add in the end of array) and pop(pops from the end of array.)
console.log("array initially: ", arr);
arr.push(100);
console.log("After push: ", arr);
arr.pop();
console.log("After pop: ", arr);

//map, filer, find
const modified_arr = arr.map(num => num*num);  //this returns a new modified array, the original array is kept unchanged.
console.log("new modified array after mapping as num=> num*num: ", modified_arr);

//filter.
const filtered_arr = arr.filter(num => num > 2)   //keep only the numbers satisfying the condition, remove the rest.
                                                  //this returns a new filtered array, original is kept as it is.
console.log("new filtered array when filtered for greater than 2: ", filtered_arr);

//find
const find_output = arr.find(num => num > 3)  //find the first number satisfying this condition.
console.log("find's output for num > 3 = ", find_output);

//FOR-EACH
arr.forEach(n => console.log(n));
arr.forEach(n => {
  const double = n*2;
  console.log(double);
});

//to print without a newline at the end.
process.stdout.write("Hello");

//Comparison operators.
0 == false      // true  ⚠️ (type coercion — JS converts types to compare)
0 === false     // false ✅ (strict — checks type AND value)

"5" == 5        // true  ⚠️
"5" === 5       // false ✅

//Rule: always use === and !==, never == or != unless you're very sure.

//what's interpreted as true and what is false;
//This passes for: 
// "", 0, null, undefined, NaN, false → all falsy. 
// Everything else (including "0" as a string, empty arrays [], empty objects {}) → truthy. *****important*****



//#######################################//
//        POSTMAN TEST WRIITING          //

/*
In POSTMAN, the chronology is:

  Pre-Request Script => Request Sent => Response Received => Post-Request Script =>  Test result.
//
THE pm Object:
pm is a global object Postman injects into your script— similar to how request/response objects
get injected in a Flask/FastAPI route handler, except here it's pre-built for you.

// --- Reading the response ---
pm.response.json()           // parses response body as JS object (most used)
pm.response.text()           // raw response body as string
pm.response.code             // status code, e.g. 200
pm.response.headers.get("Content-Type")
pm.response.responseTime     // time in ms

// --- Writing assertions ---
pm.test("Test description", () => {
    pm.expect(pm.response.code).to.equal(200);
});

// --- Variables (persist data across requests) ---
pm.environment.set("token", "abc123");     // store
pm.environment.get("token");                // retrieve
pm.collectionVariables.set("userId", 5);    // similar, scoped to collection instead
*/

/*
  REPONSE
  response is EVERYTHING that the server sends back in return of a request.
  it includes:
    --Status and code
      pm.response.status ->returns the textual HTTP status message (reason phrase) as a string. ex: "OK"
      pm.response.code -> this gives the numerical status code. ex : 200, 404 etc.
    --Headers (meta data)
      things like- content-type : applicaiton/json etc.
    --Response body : The actual data. the json part.

  pm.response.code      // 200
  pm.response.headers   // headers
  pm.response.json()    // body as JS object

*/

/*
  IMPORANT ASSERTIONS

  //equal
  pm.expect(actual).to.equal(expected);
  example: pm.expect(pm.response.code).to.equal(200);

  //not equal
  pm.expect(actual).to.not.equal(expected);
  example: pm.expect(user.name).to.not.equal("");


  //more than
  pm.expect(actual).to.be.above(value);
  pm.expect(tasks.length).to.be.above(0);


  //less than
  pm.expect(actual).to.be.below(value);
  pm.expect(price).to.be.below(100);


  //greater than or equal
  pm.expect(actual).to.be.at.least(value);
  pm.expect(score).to.be.at.least(50);

  //less than or equal to
  pm.expect(actual).to.be.at.most(value);
  pm.expect(age).to.be.at.most(60);

  //check if true
  pm.expect(actual).to.be.true;
  pm.expect(task.completed).to.be.true;

  //check if false
  pm.expect(actual).to.be.false;
  pm.expect(task.completed).to.be.false;

  //check null
  pm.expect(actual).to.be.null;

  //check non-null/undefined.
  pm.expect(actual).to.exist;
  pm.expect(response.user).to.exist;

  //check type
  pm.expect(actual).to.be.a(type);
  arguments : "string", "number", "boolean", "array", "object
                            
  //check if array includes an element.
  pm.expect(array).to.include(value);
  pm.expect(["a", "b", "c"]).to.include("b");


  //check if string includes a certain text.
  pm.expect(string).to.include(text);
  pm.expect(message).to.include("success");


  //check if object has a certain property.
  pm.expect(object).to.have.property(propertyName);
  pm.expect(user).to.have.property(name);

*/