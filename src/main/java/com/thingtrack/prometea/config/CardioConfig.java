package com.thingtrack.prometea.config;

import java.util.Properties;

import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(basePackages = { "com.thingtrack.prometea.repository.cardio" },
					   entityManagerFactoryRef = "cardioEntityManagerFactory",
					   transactionManagerRef = "cardioTransactionManager")
public class CardioConfig {	
	@Bean(name = "cardioDataSource")
	public DataSource cardioDataSource(){
      DriverManagerDataSource dataSource = new DriverManagerDataSource();
      
      dataSource.setDriverClassName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
      dataSource.setUrl("jdbc:sqlserver://192.168.1.25:1433;databaseName=PROMETEA_CardiopatiaSQL");
      dataSource.setUsername( "miguel" );
      dataSource.setPassword( "miguel" );
      
      return dataSource;
   	}
	
    @Bean(name = "cardioEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean cardioEntityManagerFactory(@Qualifier("cardioDataSource") DataSource dataSource) {
    	Properties properties = new Properties();
        properties.setProperty("hibernate.dialect", "org.hibernate.dialect.SQLServer2012Dialect");
                 
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        
        em.setDataSource(dataSource);
        em.setPersistenceUnitName("cardioPU");
        em.setPackagesToScan(new String[] { "com.thingtrack.prometea.domain.cardio" });
        em.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        em.setJpaProperties(properties);
        
        return em;
    }
	
    @Bean(name = "cardioTransactionManager")
    public PlatformTransactionManager cardioTransactionManager(@Qualifier("cardioEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
