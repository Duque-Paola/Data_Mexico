df.1 <- read.table("/home/asus/Documents/Proyectos/Covid_Economia/datos_abiertos_covid19/201128COVID19MEXICO.csv", header = TRUE, sep = ",") 
df.j <- data.frame(filter(df.1, ENTIDAD_RES == "14"))

  df.2 <- read.table("/home/asus/Downloads/2020-12-01_07-37-31.xlsx", header = TRUE, sep = "") 
X <- read.csv(url("https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"))

-
df.m <- data.frame(filter(X, country_region == "Mexico", sub_region_1 == "Jalisco"))
##########################################################################################


df_violencia <- read.table("IDEFC_NM_oct2020.csv", header = TRUE, sep = ",",check.names = F) 
names(df_violencia)
names(df_violencia) = c("Ano", "Clave_Ent", "Entidad", "Bien_Juridico_Afectado", "Tipo_delito", "Subtipo_delito", "Modalidad", "Enero",
                        "Febrero", "Marzo", "Abril" ,"Mayo", "Junio","Julio","Agosto", "Septiembre", "Octubre", "Noviembre","Diciembre")
#datos <- df.violencia

df_m_2020 <- data.frame(dplyr::filter(df_violencia, Entidad == "Jalisco", Tipo_delito == "Violencia familiar", Ano == "2020"))        
df_m_2020 <- t(subset(df_m_2020, select = Enero:Octubre, header = FALSE))
row.names(df_m_2020) <- NULL

df_m_2019 <- data.frame(dplyr::filter(df_violencia, Entidad == "Jalisco", Tipo_delito == "Violencia familiar", Ano == "2019"))        
df_m_2019 <- t(subset(df_m_2019, select = Enero:Octubre, header = FALSE))
row.names(df_m_2019) <- NULL

View(df_m_2020)
View(df_m_2019)

#plot
library(ggplot2)
library(tidyverse)
x <- c("Enero","Febrero", "Marzo", "Abril" ,"Mayo", "Junio","Julio","Agosto", "Septiembre", "Octubre")

dates <- seq(as.Date("01-01", format= "%d-%m"), length.out = 10, by = "month")
df_violencia_2020 <- data.frame(dates, df_m_2020, rep(2020,length(df_m_2020)))
names(df_violencia_2020) <- c("fecha","denuncias","año")
df_violencia_2019 <- data.frame(dates, df_m_2019, rep(2010,length(df_m_2019)))
names(df_violencia_2019) <- c("fecha","denuncias","año")
df_violencia_jalisco <- rbind(df_violencia_2020, df_violencia_2019)

ggplot(df_violencia_19_20, aes(dates)) + 
  geom_line(aes(y = X1), color = "darkred") + 
  geom_line(aes(y = X1.1), color = "blue")
  + geom_line() + scale_x_date(date_labels = "%b") 

# Make a basic graph
plot( df_violencia_19_20~a , type="b" , bty="l" , xlab="value of a" , ylab="value of b" , col=rgb(0.2,0.4,0.1,0.7) , lwd=3 , pch=17 , ylim=c(1,5) )
lines(c ~a , col=rgb(0.8,0.4,0.1,0.7) , lwd=3 , pch=19 , type="b" )

# Add a legend
legend("bottomleft", 
       legend = c("Group 1", "Group 2"), 
       col = c(rgb(0.2,0.4,0.1,0.7), 
               rgb(0.8,0.4,0.1,0.7)), 
       pch = c(17,19), 
       bty = "n", 
       pt.cex = 2, 
       cex = 1.2, 
       text.col = "black", 
       horiz = F , 
       inset = c(0.1, 0.1))
