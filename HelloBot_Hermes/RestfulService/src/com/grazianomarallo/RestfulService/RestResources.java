package com.grazianomarallo.RestfulService;

/*
  Created by grazianomarallo on 11/11/2017.
 */

import com.google.gson.Gson;
import com.grazianomarallo.RestfulService.Cafeteria.Cafeteria;
import com.grazianomarallo.RestfulService.Studyroom.StudyRoom;


import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

// The Java class will be hosted at the URI path "/restresources"
@Path("/restresources")
public class RestResources {
    // The Java method will process HTTP GET /POST requests


    @GET
    @Path("/studyrooms")
    // The Java method will produce content identified by the MIME Media type "text/plain"
    public Response getStudyRooms() {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        List<StudyRoom> studyRoomsList = new ArrayList<>(map.values());

        String Json = gson.toJson(studyRoomsList);
        if (Json == null) return Response.status(801).entity("StudyRoom  not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @GET
    @Path("/studyroom/{id}")
    public Response getStudyRoom(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        String Json = gson.toJson(map.get(id));
        if (Json == null) return Response.status(802).entity("StudyRoom not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }

    @GET
    @Path("/studyroom/info/{id}")
    public Response getInfoStudyRoom(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        String Json = gson.toJson(map.get(id).getInformations());
        if (Json == null)return Response.status(803).entity("Infos not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }





    @GET
    @Path("/studyroom/{id}/capacity")
    public Response getCapacitySr(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        String Json = gson.toJson(map.get(id).getCapacity());
        if (Json == null) return Response.status(805).entity("Capacity not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @GET
    @Path("/studyroom/{id}/takenSeats")
    public Response getTakenSeatsSr(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        String Json = gson.toJson(map.get(id).getTakenSeats());
        if (Json == null)return Response.status(806).entity("Taken Seats not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @GET
    @Path("/studyroom/coordinates")
    public Response getCoordinatesSr() {
        Gson gson = new Gson();

        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        ArrayList<BaseInfo> baseInfoArrayList = new ArrayList<>();
        for (Map.Entry<Integer,StudyRoom> c : map.entrySet()){
            BaseInfo baseInfo = new BaseInfo();
            StudyRoom sr = c.getValue();
            baseInfo.setAddress(sr.getInfo().getAddress());
            baseInfo.setCoordinates(sr.getInfo().getCoordinates());
            baseInfoArrayList.add(baseInfo);
        }
        String Json = gson.toJson(baseInfoArrayList);
        if (Json == null) return Response.status(807).entity("Coordinates not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @POST
    @Path("/studyroom/{id}/addtakenSeats")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response addTakenSeatsSr(@PathParam("id") int id,String amount) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        int seats_num = map.get(id).getTakenSeats();
        seats_num+= Integer.parseInt(amount);
        if(seats_num > map.get(id).getCapacity() )
            seats_num = map.get(id).getCapacity();
        map.get(id).setTakenSeats(seats_num);
        return Response.ok().build();
    }

    @POST
    @Path("/studyroom/{id}/subtakenSeats")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response subTakenSeatsSr(@PathParam("id") int id, String amount) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, StudyRoom> map = DataStructures.getInstance().getStudyrooms();
        int seats_num = map.get(id).getTakenSeats();
        seats_num-=Integer.parseInt(amount);
        if(seats_num < 0 )
            seats_num = 0;
        map.get(id).setTakenSeats(seats_num);
        return Response.ok().build();
    }


    @GET
    @Path("/cafeterias")
    // The Java method will produce content identified by the MIME Media type "text/plain"
    public Response getCafeterias() {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        List<Cafeteria> cafeteriasList = new ArrayList<>(map.values());

        String Json = gson.toJson(cafeteriasList);
        if (Json == null) return Response.status(801).entity("Cafeterias not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @GET
    @Path("/cafeteria/{id}")
    public Response getCafeteria(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id));
        if (Json == null) return Response.status(802).entity("Cafeteria not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }

    @GET
    @Path("/cafeteria/info/{id}")
    public Response getInfoCafeteria(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id).getInformations());
        if (Json == null)return Response.status(803).entity("Infos not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }

    @GET
    @Path("/cafeteria/{id}/menu")
    public Response getMenu(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id).getMenu());
        if (Json == null) return Response.status(804).entity("Menu not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }

    /*
    @GET
    @Path("/cafeteria/{id}/busy_level")
    public Response getCoordinates(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id).getTakenSeats());
        if (Json == null) return Response.status(800).entity("Busy level not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }
    */

    @GET
    @Path("/cafeteria/{id}/capacity")
    public Response getCapacity(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id).getCapacity());
        if (Json == null) return Response.status(805).entity("Capacity not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }




    @GET
    @Path("/cafeteria/{id}/takenSeats")
    public Response getTakenSeats(@PathParam("id") int id) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        String Json = gson.toJson(map.get(id).getTakenSeats());
        if (Json == null)return Response.status(806).entity("Taken Seats not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @GET
    @Path("/cafeterias/coordinates")
    public Response getCoordinates() {
        Gson gson = new Gson();

        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        ArrayList<BaseInfo> baseInfoArrayList = new ArrayList<>();
        for (Map.Entry<Integer,Cafeteria> c : map.entrySet()){
            BaseInfo baseInfo = new BaseInfo();
            Cafeteria cf = c.getValue();
            baseInfo.setAddress(cf.getInfo().getAddress());
            baseInfo.setCoordinates(cf.getInfo().getCoordinates());
            baseInfoArrayList.add(baseInfo);
        }
        String Json = gson.toJson(baseInfoArrayList);
        if (Json == null) return Response.status(807).entity("Coordinates not found").build();
        return Response.ok(Json, MediaType.APPLICATION_JSON).build();
    }


    @POST
    @Path("/cafeteria/{id}/addtakenSeats")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response addTakenSeats(@PathParam("id") int id,String amount) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        int seats_num = map.get(id).getTakenSeats();
        seats_num+= Integer.parseInt(amount);
        if(seats_num > map.get(id).getCapacity() )
            seats_num = map.get(id).getCapacity();
        map.get(id).setTakenSeats(seats_num);
        return Response.ok().build();
    }

    @POST
    @Path("/cafeteria/{id}/subtakenSeats")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response subTakenSeats(@PathParam("id") int id, String amount) {
        Gson gson = new Gson();
        ConcurrentHashMap<Integer, Cafeteria> map = DataStructures.getInstance().getCafeterias();
        int seats_num = map.get(id).getTakenSeats();
        seats_num-=Integer.parseInt(amount);
        if(seats_num < 0 )
            seats_num = 0;
        map.get(id).setTakenSeats(seats_num);
        return Response.ok().build();
    }










}