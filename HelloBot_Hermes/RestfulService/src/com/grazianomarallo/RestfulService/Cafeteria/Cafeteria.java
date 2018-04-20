package com.grazianomarallo.RestfulService.Cafeteria;


import com.grazianomarallo.RestfulService.BaseInfo;
import com.grazianomarallo.RestfulService.Resource;

public class Cafeteria extends Resource {
    private Menu menu;
    private BaseInfo info;



    public Cafeteria(int capacity, BaseInfo informations) {
        super(capacity, informations);
        this.info = informations;
    }




    public Menu getMenu() {
         return menu;
    }

    public void setMenu(Menu menu) {
        this.menu = menu;
    }


    public BaseInfo getInfo() {
        return info;
    }

    public void setInfo(BaseInfo info) {
        this.info = info;
    }

}
