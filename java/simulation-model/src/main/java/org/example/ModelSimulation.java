package org.example;

import org.example.events.Event;
import org.example.events.EventStack;
import org.example.events.EventType;

public class ModelSimulation {
    private final double finishTaskInterval = 0.32;
    private final double acceptTaskInterval = 0.29;
    private final double maxModellingTime = 320;
    private final int memorySize = 55;

    private TaskStack taskStack;
    private EventStack eventStack;
    private Metric metrics;
    private double currentTime;
    private Event lastEvent;

    private boolean isBusy;
    private boolean isFinished;

    public Metric getMetrics() {
        return metrics;
    }

    public ModelSimulation() {
        resetSimulation();
    }

    public void createEvent(EventType type) {
        switch (type) {
            case ACCEPT_FIRST_TASK -> eventStack.addEvent(new Event(currentTime, EventType.ACCEPT_FIRST_TASK));
            case ACCEPT_NEW_TASK -> {
                var randomInterval = new RandomExp(acceptTaskInterval).getNext();
                eventStack.addEvent(new Event(currentTime + randomInterval, EventType.ACCEPT_NEW_TASK));
            }
            case FINISH_PROCESS_TASK -> {
                var randomInterval = new RandomExp(finishTaskInterval).getNext();
                eventStack.addEvent(new Event(currentTime + randomInterval, EventType.FINISH_PROCESS_TASK));
            }
            case FINISH_MODELLING -> {
                eventStack.addEvent(new Event(maxModellingTime, EventType.FINISH_MODELLING));
            }
        }
    }

    private void resetSimulation() {
        this.taskStack = new TaskStack(memorySize);
        this.eventStack = new EventStack();
        this.metrics = new Metric();
        this.currentTime = 0;
        this.isBusy = false;
        this.isFinished = false;
    }

    private void processEvents() {
        // достаём текущий Event
        Event event = eventStack.getNextEvent();
        switch (event.getEventType()) {
            case ACCEPT_FIRST_TASK -> {
                // создаём событие поступления данных
                createEvent(EventType.ACCEPT_NEW_TASK);
            }
            case ACCEPT_NEW_TASK -> {
                // учитываем полученые задачи
                metrics.incInputTasks();
                // проверяем на заполненость
                if (taskStack.isFree()) {
                    taskStack.pushTask();
                } else {
                    // учитываем потеряные задачи
                    metrics.incMissedTasks();
                }

                currentTime = event.getTime();
                createEvent(EventType.ACCEPT_NEW_TASK);

                if (!isBusy) {
                    // вычисляем разницу между послежним Event и текущим
                    var delta = currentTime - lastEvent.getTime();
                    // учитываем простой процессора
                    metrics.incDowntime(delta);
                    isBusy = true;
                    createEvent(EventType.FINISH_PROCESS_TASK);
                }

            }
            case FINISH_PROCESS_TASK -> {
                // учитываем обработанные задачи
                metrics.incProcessedTasks();
                taskStack.popTask();
                currentTime = event.getTime();

                if (taskStack.isEmpty()) {
                    isBusy = false;
                } else {
                    createEvent(EventType.FINISH_PROCESS_TASK);
                }
            }
            case FINISH_MODELLING -> {
                if (isBusy) {
                    metrics.incProcessedTasks();
                    taskStack.popTask();
                    currentTime = event.getTime();
                    taskStack.popTask();
                    currentTime = event.getTime();
                }
                isBusy = false;
                isFinished = true;
            }
        }
        lastEvent = event;
    }

    public void runSimulation() {
        // сбрасываем симуляцию
        resetSimulation();

        createEvent(EventType.ACCEPT_FIRST_TASK);
        createEvent(EventType.FINISH_MODELLING);    // добавляем будущее событие завершения моделирования

        while (!isFinished) processEvents();

        System.out.println("Фактическое F" + String.valueOf(currentTime));
    }
}
