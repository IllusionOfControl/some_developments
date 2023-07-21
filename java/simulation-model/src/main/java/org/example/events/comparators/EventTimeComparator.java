package org.example.events.comparators;

import org.example.events.Event;

import java.util.Comparator;

public class EventTimeComparator implements Comparator<Event> {

    @Override
    public int compare(Event event1, Event event2) {
        if (event1.getTime() < event2.getTime()) {
            return 1;
        } else if (event1.getTime() > event2.getTime()) {
            return -1;
        } else {
            return 0;
        }
    }
}
