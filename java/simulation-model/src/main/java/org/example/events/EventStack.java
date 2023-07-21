package org.example.events;

import org.example.events.comparators.EventPriorityComparator;
import org.example.events.comparators.EventTimeComparator;

import java.util.Collections;
import java.util.Stack;

public class EventStack {
    private Stack<Event> stack;

    public EventStack() {
        stack = new Stack<Event>();
    }

    public void addEvent(Event event) {
        stack.push(event);
    }

    public Event getNextEvent() {
        // Сортируем Events по времени
        EventTimeComparator comparator = new EventTimeComparator();
        Collections.sort(stack, comparator);
        //возвращаем самое ближайшее по времени
        return stack.pop();
    }

    public Event getPriorityEvent() {
        // Сортируем Events по приоритету типа Event
        EventPriorityComparator comparator = new EventPriorityComparator();
        Collections.sort(stack, comparator);

        // Возвращаем самое высокое по приоритету
        return stack.pop();
    }

    public boolean isEmpty() {
        return stack.isEmpty();
    }

    @Override
    public String toString() {
        return "EventStack{\n" +
                "\tstack=\n" + stack +
                "}\n";
    }
}