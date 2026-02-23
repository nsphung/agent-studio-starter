FROM node:22.22-trixie-slim

ENV NEXT_TELEMETRY_DISABLED=1

# Copy package.json and package-lock.json
COPY package*.json ./

# Install npm production packages 
RUN npm install --production

COPY . /opt/app-root/src
WORKDIR /opt/app-root/src

# ENV NODE_ENV production
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "dev"]