# Use Node.js as a parent image
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
COPY ./FinancialClient/financial-analyzer-client/package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the client's source code
COPY ./FinancialClient/financial-analyzer-client .

# Make port 7001 available to the world outside this container
EXPOSE 7001

# Run npm start when the container launches
CMD ["npm", "start"]
