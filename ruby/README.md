# Ruby Example Code

bundle install

To run each script you can simply open up two terminals and navigate to the project folder. In the first terminal you can run:

```ruby
ruby publisher.rb
```

Then in the other terminal you can start the consumer:

```ruby
ruby consumer.rb
```

The consumer.rb script keeps running until you close it, unlike publisher.rb. This means it can instantly consume any messages published to the queue. (To quit consumer.rb you can press CTRL+c in your terminal)

In reality it's best to keep the connection alive in both the publisher and consumer scripts, rather than opening and closing it repeatedly. This is because opening and closing connections is considered "expensive".


