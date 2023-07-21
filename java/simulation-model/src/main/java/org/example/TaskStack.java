package org.example;

public class TaskStack {
    private final int memorySize;
    private int memoryFree;

    public TaskStack(int memorySize) {
        this.memorySize = memorySize;
        this.memoryFree = memorySize;
    }

    public boolean isFree() {
        return memoryFree > 0;
    }

    public boolean isEmpty() {
        return memoryFree == memorySize;
    }

    public void pushTask() {
        if (isFree()) memoryFree--;
        else throw new StackOverflowError();
    }

    public void popTask() {
        if (!isEmpty()) memoryFree++;
        else throw new StackOverflowError();
    }
}