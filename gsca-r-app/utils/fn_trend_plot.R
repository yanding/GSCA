trend_plot <- function(data,aesx,aesy,linecolor,linetype,xlabels,facetgrid="symbol~cancertype",colorname,color_list,fillbreaks,color_lables,title,xlab,ylab){
  data %>%
    ggplot(aes_string(x=aesx,y=aesy)) +
    geom_line(aes_string(color=linecolor,linetype=linetype),size=2) +
    facet_grid( as.formula(facetgrid),scales = "free_y") +
    scale_x_continuous(labels= xlabels) +
    labs(title = title) +
    xlab(xlab) +
    ylab(ylab) + 
    scale_color_gradient2(
      name = colorname, # "Methylation diff (T - N)",
      n.breaks=10,
      low = color_list[3],
      high = color_list[1],
      mid =  color_list[2],
      midpoint = 0,
      limits=c(min(fillbreaks),max(fillbreaks)),
      breaks=fillbreaks,
      labels=color_lables
    ) +
    theme(
      panel.background = element_rect(colour = "grey", fill = "white"),
      panel.grid = element_blank(),
      panel.grid.major = element_blank(),
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      axis.title.y = element_blank(),
      axis.text.x = element_text(size = 10,colour = "black"),
      legend.text = element_text(size = 10),
      axis.title = element_text(size=12),
      legend.title = element_text(size = 12),
      legend.key = element_rect(fill = "white", colour = "black"),
      legend.key.size = unit(0.5, "cm"),
      plot.title = element_text(size = 14),
      strip.background =  element_blank(),
      strip.text = element_text(color="black",size = 12),
      panel.spacing = unit(0.1, "lines"),
      strip.text.y = element_text(angle = 0,hjust = 0,vjust = 0.5)
    ) -> p
  return(p)
}
