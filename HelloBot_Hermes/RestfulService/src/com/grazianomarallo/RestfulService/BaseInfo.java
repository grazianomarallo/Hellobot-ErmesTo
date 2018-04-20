package com.grazianomarallo.RestfulService;

/**
 * Basic info handling
 */
public class BaseInfo {
    private String name;
    private String address;
    private Coordinates coordinates;
    private Time launch, dinner,open_time;

    public BaseInfo(String name, String address, Time launch, Time dinner, Coordinates coordinates) {
        this.name = name;
        this.address = address;
        this.coordinates = coordinates;
        this.launch = launch;
        this.dinner = dinner;
    }

    public BaseInfo(String name, String address, Time open_time, Coordinates coordinates) {
        this.name = name;
        this.address = address;
        this.coordinates = coordinates;
        this.open_time = open_time;
    }




    public static class Time {
        private  String start, end;



        public Time(String start, String end) {
           this.start = start;
           this.end = end;
         }

        public String getStart() {
            return start;
        }

        public void setStart(String start) {
            this.start = start;
        }

        public String getEnd() {
            return end;
        }

        public void setEnd(String end) {
            this.end = end;
        }

    }




    public BaseInfo() {

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(Coordinates coordinates) {
        this.coordinates = coordinates;
    }
}


