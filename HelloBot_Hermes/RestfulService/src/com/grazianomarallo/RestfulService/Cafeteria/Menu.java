package com.grazianomarallo.RestfulService.Cafeteria;

import java.util.ArrayList;

/**
 * Created by grazianomarallo on 11/11/2017.
 */
public class Menu {
    private ArrayList<Dish> first_plate;
    private ArrayList<Dish>  second_plate;



    public Menu(ArrayList<Dish> first_plate, ArrayList<Dish> second_plate) {
        this.first_plate = first_plate;
        this.second_plate = second_plate;
    }

    public ArrayList<Dish> getFirst_plate() {
        return first_plate;
    }

    public void setFirst_plate(ArrayList<Dish> first_plate) {
        this.first_plate = first_plate;
    }

    public ArrayList<Dish> getSecond_plate() {
        return second_plate;
    }

    public void setSecond_plate(ArrayList<Dish> second_plate) {
        this.second_plate = second_plate;
    }



}
