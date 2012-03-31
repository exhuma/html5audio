HTML5 Audio Sandbox
===================

This project is a small tool in which I experiment with audio streaming
alternatives. The goal is to have the same audio-content sent/streamed to
multiple targets.

The overall design is to have a single data "generator" where optional
"consumers" can hook to. After a consumer hooked itself into the generator,
the generator will start providing data to this consumer.

This is a rewrite of an initial, promising attempt. The main problems I had in
the initial attempt were the following:

* When a web-request came in, for some reasons, two consumers were added. The
  source of this is still unknown.

* I had no means to detect when a consumer has gone away. Especially in the
  case of a web client. One idea is to make the web-client send heartbeats to
  the server. If no heartbeat has been recieved in a set amount of time, the
  consumer will be disconnected.

Thinks that I will *not* (yet) tackle are:

* transcoding
* file management (initially I'll work with ``/dev/urandom`` as "audio"
  source)
* Audio metadata
* any form of visual design




