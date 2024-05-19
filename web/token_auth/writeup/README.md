# Token auth solution

## Suspicious function

`mergeInto()` function is used only once, merging the body of the request with an almost empty object. It is a very unnatural way of restricting the parameters of an object. The function merges a source into a target in recursive way without any key validation. It can lead to **prototype pollution** vulnerability.

## Prototype pollution

It occurs when user is able to inject properties to prototype of an object. Javascript, stores **reference** to the parent of object under `__proto__` key. This means, that changing one prototype, will affect all objects that inherit from it.

## Object properties

If we tried to access a property that object didn't have, it would search for it in its prototype chain. So if we added property `admin = true` to the prototype of `Object()`, then all objects that inherit from it and do not have their own property `admin`, would get new property `admin = 1`.

## Attack

Our goal is to set `Object().__proto__.admin = 1`. Then, by calling GET `/flag` without any authorization cookie, `token` variable will be empty, so `data` will be equal to `{}` and `data.admin` will be true.

## Payload

Arguments of `mergeInto()` function are `req.body` and `restricted`. We can control body of the `/login` POST request, and pass `__proto__` as parameter of username:

```json
{
  "username": {
    "__proto__": {
      "admin": true
    }
  },
  "password": "test"
}
```

The merging function will then set `admin` property of `Object()` prototype to true. This will work only if there is a user with that username and password in the database. In order to add one, we first send exactly the same request, but to `/register` endpoint that will create such user. Finally, by requesting GET from `/flag`, we get the flag: `BtSCTF{W4tch_0ut,pr0t0typ3_15_th3r3!}`