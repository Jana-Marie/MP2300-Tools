thickness = 12;

color("blue")
penHolder();
//translate([0,0,9])
//color("green")
//penHolderRing();
//for(i = [0:1:10]){
//    translate([0,0,(i*1)+19])
//    washer(15,thickness);
//}

module penHolderRing(){
    $fn=50;
    //holder
    h=10;
    d=thickness;
    d_hole=15;
    //pen
    difference(){
        union(){
            translate([0,0,0])cylinder(d=d,h=h);
        }union(){
            translate([0,0,-0.1])cylinder(d=d_hole,h=h+0.2);
        }
    }
}

module penHolder(){
    $fn=500;
    //holder
    h=37;
    d=11;
    d_top=thickness;
    h_ring=27.5;
    t_ring=1.2;
    d_ring=15;
    h_tip=5;
    //pen
    d_hole_lower=2.7;
    d_hole_upper=6.2;
    h_hole=5;
    difference(){
        union(){
            translate([0,0,h_tip])cylinder(d=d,h=h-h_tip);
            translate([0,0,0])cylinder(d1=d/3,d2=d,h=h_tip);
            translate([0,0,h_ring])cylinder(d=d_ring,h=t_ring);
            translate([0,0,h_ring+t_ring])cylinder(d=d_top,h=h-t_ring-h_ring);
        }union(){
            translate([0,0,-0.1])cylinder(d=d_hole_lower,h=h+0.2);
            translate([0,0,h_hole])cylinder(d=d_hole_upper,h=h);
            translate([0,0,h-3])rotate([90,0,0])cylinder(d=2.3,h=d);
        }
    }
}

module washer(_d1,_d2){
    $fn=50;
    h=1;
    difference(){
        union(){
            color("silver")
            translate([0,0,0])cylinder(d=_d2,h=h);
        }union(){
            translate([0,0,-0.1])cylinder(d=_d1,h=h+0.2);
        }
    }
}
