import { Meteor } from 'meteor/meteor';
import { check } from 'meteor/check';
import { AsteroidCollection } from '/imports/api/asteroids';

async function insertAsteroid({ name, size, speed, description }) {
  await AsteroidCollection.insertAsync({ name, size, speed, description, createdAt: new Date() });
}

Meteor.startup(async () => {
  /* Clear the collection */
  await AsteroidCollection.removeAsync({});

  await insertAsteroid({
    name: "Ceres",
    size: 940,
    speed: 17.9,
    description: "A very cool asteroid."
  });

  await insertAsteroid({
    name: "Pallas",
    size: 544,
    speed: 15.2,
    description: "It goes really fast."
  });

  await insertAsteroid({
    name: "Juno",
    size: 246,
    speed: 13.8,
    description: "My personal favorite."
  });

  await insertAsteroid({
    name: "Vesta",
    size: 525,
    speed: 19.3,
    description: "I don't like this one."
  });

  await insertAsteroid({
    name: "[[REDACTED]]",
    size: 0,
    speed: 0,
    description: "BtSCTF{4st3r01ds_4r3_v3ry_c00l}"
  })
});

Meteor.methods({
  getPurpose(about) {
    check(about, String);

    if (about === 'learn_more') {
      return "asteroid collection";
    }
  },
  getAsteroidNames() {
    return AsteroidCollection.find({}, { fields: { name: 1 } }).fetch();
  },
  getSize(name) {
    check(name, String);

    const asteroid = AsteroidCollection.findOne({ name });

    if (asteroid) {
      return asteroid.size;
    }
  },
  getSpeed(data, in_meters) {
    check(data, Object);
    check(in_meters, Boolean);

    const asteroid = AsteroidCollection.findOne(data);

    if (asteroid) {
      return in_meters ? asteroid.speed : asteroid.speed * 3600;
    }
  }
});
