package org.example.events;


public class Event {
    private double time;
    private EventType eventType;

    public Event(double time, EventType eventType) {
        this.time = time;
        this.eventType = eventType;
    }

    public double getTime() {
        return time;
    }

    public void setTime(double time) {
        this.time = time;
    }

    public EventType getEventType() {
        return eventType;
    }

    public void setEventType(EventType eventType) {
        this.eventType = eventType;
    }

    @Override
    public String toString() {
        return "Event{" +
                "time=" + time +
                ", eventType=" + eventType +
                "}\n";
    }
}
