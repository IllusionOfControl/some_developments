package org.example.events.comparators;

import org.example.events.Event;
import org.example.events.EventType;

import java.util.Comparator;

public class EventPriorityComparator implements Comparator<Event> {

    @Override
    public int compare(Event event1, Event event2) {
        if (event1.getEventType() == EventType.FINISH_MODELLING) {
            return 1; // task1 has max priority
        } else if (event2.getEventType() == EventType.FINISH_MODELLING) {
            return -1; // task2 has max priority
        } else if (event1.getEventType() == EventType.FINISH_PROCESS_TASK) {
            return 1; // task1 has max priority
        } else if (event2.getEventType() == EventType.FINISH_PROCESS_TASK) {
            return -1; // task2 has max priority
        } else {
            return 0;
        }
    }
}
