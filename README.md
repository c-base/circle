circle-app
==========

circle management and standardized protocol generation app

Request For Comments
====================

## Abstract

The circle-app is a web-application. It's primary focus is to provide a rich tool-set for organizing and running the
circle-event, as well as generating written transcript protocols of circle-events in standardized output formats.

The circle-app must help the circle-members organize the circle-event by providing useful and convenient
tool-chains, while not limiting the circle-members in their decisions how any special edge-case may be handled. Even
the possibility to overrule the fundamental rule-set of the formal protocol, must be possible under any circumstances.
However, breaking the formal rules must be made explicitly transparent within the end-result protocol and thus in any of
its standardized output formats.

The primary focus for the standardized output formats should be the generation of an e-mail body. This e-mail body
should be primarily designed to be sent to e.g. the mailing-list and should be targeted towards regular c-base members.
This means, it should be readable, clearly arranged and breaks from the rules should be made explicitly transparent.
Even members who do not know the formal protocol of the circle-event should intuitively be able to understand the
transcript protocol and its abstract outcomes.

The circle-app must provide search-ability wherever it makes sense. It also should provide abstract ways of
inter-connecting topics, such as follow-ups, abolishments, nullifications and others - making such relations easily
reachable from one another.

## Life-Cycles

### Circle Phasing

Let's talk about the life-cycle of a circle-event.

#### Collection phase

There is always exactly one upcoming circle-event. This event serves as topic collection bin (see: Topic Proposal
Phase).

#### Opening phase

The initial participation-list is created, transcript writers and moderator are selected and the formal list of topics
is selected. Finally, the circle-meeting is formally opened by the moderator.

At this point the date of the circle, as well as the timestamp of the formal opening, are written into the circle-event.
In the same moment a new upcoming circle-event is initialized as a collection bin for the upcoming meeting.

#### Meeting Phase

The circle-meeting takes place and goes through all the formally selected topics (see: Topic Phasing for the
life-cycles of topics).

#### Closing phase

The circle eventually reaches the point, where all topics have been discussed.

At this point the transcript writers have a last chance to edit the entire protocol. They should be able to edit
anything - such as text, votings, results, timestamps, etc. They should also be able to generate test outputs or
send test-mails to themselves while finalizing the protocol in this phase.

The circle ends when the moderator formally closes the event. At this point the entire protocol should be made
persistent in the database and unchangeable through the front-end.

There is now no more open circle-event in the database, thus the collection bin now may be formally opened at any time.

### Topic Phasing

Let's talk about the life-cycle of a topic.

#### Proposal Phase

Any carbon-unit can propose a topic for the next circle-event and when doing so should receive explicit instructions on
the further steps to take for pushing the topic towards a formal voting. These instructions should also include the
standard info-foobar, such as for instance the c-base video-/audio-recording policy.

A topic may be proposed at any given point in time. However, there should be a dead-line for topics. Proposals past that
dead-line should be explicitly marked as PAST-DEADLINE PROPOSAL and should be postponed to the next circle-meeting by
the circle-members (see: Circle Opening Phase).

It should be made possible to un-/subscribe to incoming proposals with an @c-base.org e-mail address. It should be made
possible to filter such subscriptions to only certain categories of topics.

New proposals are linked to the collection bin (see: Circle Collection Phase).

#### Selection Phase

During the opening phase of the circle-event, the topics for the event are formally selected upon. They may be either
accepted, declined or postponed.

* When a proposal is accepted it goes into discussion phase.
* When a proposal is declined it will be closed.
* When a proposal is postponed it is closed and an open copy of the proposal is copied over into the topic collection
  bin.

#### Discussion Phase

The discussion phase starts when the timestamp of the formal opening is written into the topic. There may only exist
one open topic at any given point in time.

During the discussion phase the transcript writers create a written protocol of the discussion. The interface should
behave like an etherpad text-area.

During discussion phase a topic may be closed, proposed for voting or proposed for a general poll.

* When a topic is closed without voting or poll, it would probably be called info-topic and explicitly mark as such.
* When a topic is proposed for voting it goes into voting phase.
* When a topic is proposed for general poll it goes into poll phase.

#### Voting Phase

This phase starts when a transcript writer creates a voting for a topic. The voting and its outcomes should be formally
and logically correct or explicitly and transparently marked if otherwise.

Every voting has a formal proposal. The number of votes should sum up to the number of attending circle-members or be
explicitly and transparently marked if otherwise.

Circle-members can vote for either pro, contra or neutral.

The successful voting automatically closes the topic.

#### Poll Phase

This phase starts when a transcript writer creates a poll for a topic.

Any attending member can participate in a general poll and vote for either pro, contra or neutral.

The successful poll automatically closes the topic.

#### Closing Phase

The timestamp of the formal closing is written to the database. This leaves no open topic allowing for another topic to
be formally opened.
