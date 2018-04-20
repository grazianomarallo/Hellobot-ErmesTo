package com.grazianomarallo.RestfulService.Cafeteria;

/**
 * Created by grazianomarallo on 11/11/2017.
 */
public class Dish {
    boolean glutenFree;
    String name;
    boolean  piatto_unico;



    public Dish(boolean glutenFree, String name, boolean piatto_unico) {
        this.glutenFree = glutenFree;
        this.name = name;
        this.piatto_unico = piatto_unico;
    }



    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isGlutenFree() {
        return glutenFree;
    }

    public void setGlutenFree(boolean glutenFree) {
        this.glutenFree = glutenFree;
    }

    public boolean isPiatto_unico() {
        return piatto_unico;
    }

    public void setPiatto_unico(boolean piatto_unico) {
        this.piatto_unico = piatto_unico;
    }



}
