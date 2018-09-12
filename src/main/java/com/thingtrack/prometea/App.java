package com.thingtrack.prometea;

import java.util.List;
import org.jboss.logging.Logger;

import org.hibernate.annotations.common.util.impl.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.thingtrack.prometea.controller.PatientController;
import com.thingtrack.prometea.domain.Patient;

@SpringBootApplication
public class App {
	 private static Logger LOG = LoggerFactory.logger(App.class);
	 
	 @Autowired
	 private PatientController patientController;
	 
	 public static void main(String[] args) {
        LOG.info("STARTING THE APPLICATION");
        SpringApplication.run(App.class, args);
        LOG.info("APPLICATION FINISHED");
	 }
	 
	 public void run(String... args) {
		 List<Patient> patients = patientController.getAllPatients();
	 }
}
