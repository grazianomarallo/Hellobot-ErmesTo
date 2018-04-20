package com.grazianomarallo.RestfulService;

import com.google.gson.Gson;
import com.grazianomarallo.RestfulService.Cafeteria.Cafeteria;
import com.grazianomarallo.RestfulService.Cafeteria.Dish;
import com.grazianomarallo.RestfulService.Cafeteria.Menu;
import com.grazianomarallo.RestfulService.Studyroom.StudyRoom;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class DataStructures {
    private static DataStructures instance = null;
    private ConcurrentHashMap<Integer, Cafeteria> cafeterias = new ConcurrentHashMap<>();
    private ConcurrentHashMap<Integer, StudyRoom> studyrooms = new ConcurrentHashMap<>();
    private ArrayList<Dish> first_plate = new ArrayList<>();
    private ArrayList<Dish> second_plate = new ArrayList<>();
    private ArrayList<Dish> first_plate1 = new ArrayList<>();
    private ArrayList<Dish> second_plate1 = new ArrayList<>();
    private ArrayList<Dish> first_plate2 = new ArrayList<>();
    private ArrayList<Dish> second_plate2 = new ArrayList<>();
    private ArrayList<Dish> first_plate3 = new ArrayList<>();
    private ArrayList<Dish> second_plate3 = new ArrayList<>();
    private ArrayList<Dish> first_plate4 = new ArrayList<>();
    private ArrayList<Dish> second_plate4 = new ArrayList<>();
    private Menu menu = new Menu(first_plate,second_plate);






    /**
    Constructor for Cafetieia and Study Room
     */
    public ConcurrentHashMap<Integer, Cafeteria> getCafeterias() {
        return cafeterias;
    }

    public ConcurrentHashMap<Integer, StudyRoom> getStudyrooms() {
        return studyrooms;
    }

    private ArrayList<Dish> first_plate(){
        return first_plate;
    }
    private ArrayList<Dish> second_plate(){
        return first_plate;
    }


    protected DataStructures() {
        instantiateStructures();
        // Exists only to defeat instantiation.
    }

    //Singleton
    public static DataStructures getInstance() {
        if(instance == null) {
            instance = new DataStructures();
        }
        return instance;
    }

    /**
     * Populate Map

     */

    private void instantiateStructures(){
/*
        first_plate.add(new Dish(false,"Ragu",false));
        first_plate.add(new Dish(true,"Riso in bianco",false));
        first_plate.add(new Dish(false,"Spaghetti allo scoglio",false));
        second_plate.add(new Dish(false,"Pesce spada con patate",false));
        second_plate.add(new Dish(true,"Hamburger con crema di carote",false));
        second_plate.add(new Dish(false,"Nuggets di pollo con patatine fritte",false));

        Cafeteria c = new Cafeteria(114,new BaseInfo("Borsellino",
                "Via Paolo Borsellino, 42 - 10138 Torino", new BaseInfo.Time("12:00","15:00") , new BaseInfo.Time("19:00","21:00"), new Coordinates("45.0653015", "7.659145200000012")));
        c.setMenu(menu);
        cafeterias.put(0,c);


        first_plate1.add(new Dish(false,"Bucatini",false));
        first_plate1.add(new Dish(true,"Pennette al pesto ",false));
        first_plate1.add(new Dish(false,"Trofie alla panna",false));
        second_plate1.add(new Dish(true,"Coscia di pollo",false));
        second_plate1.add(new Dish(false,"Arrosto di maiale",true));
        second_plate1.add(new Dish(true,"Bastoncini di merluzzo",false));
        Menu m1 = new Menu(first_plate1,second_plate1);


        Cafeteria c1 = new Cafeteria(350,new BaseInfo("Castelfidardo",

                "C.so Castelfidardo, 30/A - 10128 Torino", new BaseInfo.Time("12:00","15:00") , new BaseInfo.Time("19:00","21:00"), new Coordinates("45.066165", "7.657150199999933")));
        c1.setMenu(m1);
        cafeterias.put(1,c1);


        first_plate2.add(new Dish(false,"Pizza",true));
        first_plate2.add(new Dish(true,"Bucatini alla amatriciana",false));
        first_plate2.add(new Dish(false,"Farfalle con panna e prosciutto",false));
        second_plate2.add(new Dish(true,"Polenta",false));
        second_plate2.add(new Dish(false,"Pesce Spada",true));
        second_plate2.add(new Dish(true,"Cus Cus",false));
        Menu m2= new Menu(first_plate2,second_plate2);

        Cafeteria c2 = new Cafeteria(150,new BaseInfo("Galliari",
                "Via Ormea 11 bis/e - 10125 Torino", new BaseInfo.Time("12:00","15:00") , new BaseInfo.Time("19:00","21:00"), new Coordinates("45.0582907", "7.685056499999973")));
        c2.setMenu(m2);
        cafeterias.put(2,c2);



        first_plate3.add(new Dish(false,"Pappardelle ai funghi",true));
        first_plate3.add(new Dish(true,"Lasagne",false));
        first_plate3.add(new Dish(false,"Parmiggiana",false));
        second_plate3.add(new Dish(true,"Petto di pollo a limone",false));
        second_plate3.add(new Dish(true,"Hamburger di soia",true));
        second_plate3.add(new Dish(true,"Straccetti rucola e grana",false));
        Menu m3 = new Menu(first_plate3,second_plate3);


        Cafeteria c3 = new Cafeteria(170,new BaseInfo("Olimpia",
                "Lungo Dora Siena, 102/B - 10153 Torino",  new BaseInfo.Time("12:00","15:00") , new BaseInfo.Time("19:00","21:00"),new Coordinates("45.074478", "7.701235499999939")));
        c3.setMenu(m3);
        cafeterias.put(3,c3);


        first_plate4.add(new Dish(false,"Lasagne Bianche",true));
        first_plate4.add(new Dish(true,"Pasta al forno",false));
        second_plate4.add(new Dish(true,"Pizza",true));
        second_plate4.add(new Dish(true,"Arrosto di maiale",false));
        Menu m4 = new Menu(first_plate4,second_plate4);

        Cafeteria c4 = new Cafeteria(240,new BaseInfo("Principe Amedeo",
                "Via Principe Amedeo 48 - 10123 Torino ", new BaseInfo.Time("12:00","15:00") , new BaseInfo.Time("19:00","21:00"), new Coordinates("45.0659074", "7.69230349999998")));
        c4.setMenu(m4);
        cafeterias.put(4,c4);


*/

        String a = DataStructures.usingBufferedReader("/Users/grazianomarallo/Git/HelloBot_Hermes/RestfulService/src/Cafe.txt");

        Gson gson = new Gson();
        Cafeteria[] mcArray = gson.fromJson(a,Cafeteria[].class);
        List<Cafeteria> mcList = Arrays.asList(mcArray);
       for(int i=0; i <mcList.size(); i++){
           cafeterias.put(i,mcList.get(i));

       }

        System.out.println("Size array "+mcList.size());
        for (Cafeteria c : mcList){
            System.out.println("Capacità "+c.getInfo().getCoordinates().getLatitude());
        }



        String r = DataStructures.usingBufferedReader("/Users/grazianomarallo/Git/HelloBot_Hermes/RestfulService/src/Studyrooms.txt");

        Gson gson2 = new Gson();
        StudyRoom[] mcArray1 = gson2.fromJson(r,StudyRoom[].class);
        List<StudyRoom> mcList1 = Arrays.asList(mcArray1);
        for(int i=0; i <mcList1.size(); i++){
            studyrooms.put(i,mcList1.get(i));

        }



/*
        StudyRoom r = new StudyRoom(150, new BaseInfo("Aula Studio 1", "Corso Duca Degl\'Abruzzi 24 - 10129 Torino", new BaseInfo.Time("8:00","19:30"), new Coordinates("45.0624921","7.662202999999977")));
        studyrooms.put(0,r);

        StudyRoom r1 = new StudyRoom(170, new BaseInfo("Aula Studio 2", "Corso Duca Degl\'Abruzzi 24 - 10129 Torino", new BaseInfo.Time("8:00","19:30"), new Coordinates("45.0624921","7.662202999999977")));
        studyrooms.put(1,r1);

        StudyRoom r2 = new StudyRoom(200, new BaseInfo("Aula Studio 3", "Corso Duca Degl\'Abruzzi 24 - 10129 Torino", new BaseInfo.Time("8:00","19:30"), new Coordinates("45.0624921","7.662202999999977")));
        studyrooms.put(2,r2);

        StudyRoom r3 =  new StudyRoom(70, new BaseInfo("Aula Studio 4", "Corso Duca Degl\'Abruzzi 24 - 10129 Torino", new BaseInfo.Time("8:00","19:30"), new Coordinates("45.0624921","7.662202999999977")));
        studyrooms.put(3,r3);
*/




    }


    private static String usingBufferedReader(String filePath)
    {
        StringBuilder contentBuilder = new StringBuilder();
        BufferedReader br;
        try
        {
            br = new BufferedReader(new FileReader(filePath));
            String sCurrentLine;
            while ((sCurrentLine = br.readLine()) != null)
            {
                contentBuilder.append(sCurrentLine);
            }
            br.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return contentBuilder.toString();
    }

}