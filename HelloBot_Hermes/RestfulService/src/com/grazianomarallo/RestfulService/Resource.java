package com.grazianomarallo.RestfulService;

/**
 * Created by grazianomarallo on 11/11/2017.
 */

public abstract class Resource {
    private int capacity;
    private int takenSeats;
    private BaseInfo informations;

    public Resource(int capacity, BaseInfo informations) {
        this.capacity = capacity;
        this.takenSeats = 0;
        this.informations = informations;
    }



    public int getCapacity() {
        return capacity;
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public int getTakenSeats() {
        return takenSeats;
    }

    public void setTakenSeats(int takenSeats) {
        this.takenSeats = takenSeats;
    }

    public BaseInfo getInformations() {
        return informations;
    }

    public void setInformations(BaseInfo informations) {
        this.informations = informations;
    }


}
