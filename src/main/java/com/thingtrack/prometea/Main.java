package com.thingtrack.prometea;

import org.jboss.logging.Logger;

import org.hibernate.annotations.common.util.impl.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Main implements CommandLineRunner {
	 private static Logger LOG = LoggerFactory.logger(Main.class);
	 
	 @Autowired
	 private com.thingtrack.prometea.repository.cardio.PatientRepository cardioPatientRepository;
	 
	 @Autowired
	 private com.thingtrack.prometea.repository.prometea.PatientRepository prometeaPatientRepository;
	 
	 public static void main(String[] args) {
        LOG.info("STARTING THE APPLICATION");
        SpringApplication.run(Main.class, args);
        LOG.info("APPLICATION FINISHED");
	 }	
	 	 
	 @SuppressWarnings("deprecation")
	 @Override
	 public void run(String... args) {
		LOG.info("EXECUTING : command line runner");
		  
        for (int i = 0; i < args.length; ++i) {
            LOG.info("args[{}]: {}", new Object[]{i, args[i]});
        }
		
        if (cardioPatientRepository != null)
        	cardioPatientRepository.findAll();
        
		if (prometeaPatientRepository != null)
			prometeaPatientRepository.findAll();
	 }
}
