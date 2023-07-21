package org.example;

import java.util.Random;

public class RandomExp {
    private Random random;
    private double lambda;

    public RandomExp(double lambda) {
        random = new Random();
        this.lambda = lambda;
    }

    public double getNext() {
        return  Math.log(1-random.nextDouble())/(-lambda);
    }
}
