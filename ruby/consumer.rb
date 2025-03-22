require "amqp-client"
require "dotenv/load"

# Opens and establishes a connection, channel is created automatically
client = AMQP::Client.new(ENV['CLOUDAMQP_URL']).start

# Declare a queue
queue = client.queue "email.notifications"

counter = 0
# Subscribe to the queue
queue.subscribe() do |msg|
  counter += 1
  # Add logic to handle the message here...
  puts "[📤] Message received [#{counter}]: #{msg.body}"
  # Acknowledge the message
  msg.ack
rescue => e
  puts e.full_message
  msg.reject(requeue: false)
end

# Close the connection when the script exits
at_exit do 
  client.stop
  puts "[❎] Connection closed"
end

# Keep the consumer running
sleep
