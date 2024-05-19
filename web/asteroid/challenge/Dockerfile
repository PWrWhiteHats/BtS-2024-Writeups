FROM geoffreybooth/meteor-base:2.15

# Copy app package.json and package-lock.json into container
COPY ./app/package*.json $APP_SOURCE_FOLDER/

RUN bash $SCRIPTS_FOLDER/build-app-npm-dependencies.sh

# Copy app source into container
COPY ./app $APP_SOURCE_FOLDER/

RUN bash $SCRIPTS_FOLDER/build-meteor-bundle.sh

FROM meteor/node:14.21.4-alpine3.17

ENV APP_BUNDLE_FOLDER /opt/bundle
ENV SCRIPTS_FOLDER /docker

# Runtime dependencies
RUN apk --no-cache add \
		bash \
		ca-certificates

# Copy in entrypoint
COPY --from=0 $SCRIPTS_FOLDER $SCRIPTS_FOLDER/

# Copy in app bundle
COPY --from=0 $APP_BUNDLE_FOLDER/bundle $APP_BUNDLE_FOLDER/bundle/

RUN bash $SCRIPTS_FOLDER/build-meteor-npm-dependencies.sh

# Prepare mongodb
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories

RUN apk --no-cache add mongodb
RUN mkdir -p /data/db

EXPOSE 3000

ENV ROOT_URL=${APP_ROOT_URL:-http://localhost}
ENV MONGO_URL=mongodb://localhost:27017/meteor
ENV PORT=3000

# Prepare a fixed entrypoint
RUN mv /docker/entrypoint.sh /docker/entrypoint.sh.orig
COPY start-mongo.sh /docker/entrypoint.sh
RUN cat /docker/entrypoint.sh.orig >> /docker/entrypoint.sh
RUN chmod +x /docker/entrypoint.sh

# Start app
ENTRYPOINT ["/docker/entrypoint.sh"]

CMD ["node", "main.js"]
