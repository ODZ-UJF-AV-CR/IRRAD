$fn=50;

use <./../../../../../Library/Graphics/MLAB_logo.scad>

module short_logo(){
    color("white")  
    minkowski()
    {
     cube([50,25,2]);
     cylinder(r=2,h=1);
    }

    color("black")        
    union (){
        translate ([25, 12.5, 3])  // ODROIDs passive components hole.
            scale(v = [0.25, 0.25, 0.25])
                MLAB_logo_short();
    }            
}

module long_logo(){
    color("white")  
    minkowski()
    {
     cube([100,25,2]);
     cylinder(r=2,h=1);
    }

    color("black")        
    union (){
        translate ([50, 12.5, 1])  // ODROIDs passive components hole.
            scale(v = [0.75, 0.75, 0.75])
                MLAB_logo_long();
    }            
}

module short_logo(){
    color("white")  
    minkowski()
    {
     cube([50,25,2]);
     cylinder(r=2,h=1);
    }

    color("black")        
    union (){
        translate ([25, 12.5, 3])  // ODROIDs passive components hole.
            scale(v = [0.25, 0.25, 0.25])
                MLAB_logo_short();
    }            
}

//short_logo();
long_logo();

//text("IRRAD01A");
