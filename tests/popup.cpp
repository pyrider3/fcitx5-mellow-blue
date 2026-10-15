#include "../src/motion.h"
#include <cassert>
#include <iostream>
int main() {
    smoothui::PopupFade f;assert(f.opacity(0)==0);
    f.open(1000);assert(f.opacity(1000)==0);
    assert(f.offset(1000)==2);
    double middle=f.opacity(46000);assert(middle>0 && middle<1);
    f.open(46000);assert(f.began==1000); // typing refresh does not replay
    assert(!f.step(91000));assert(f.opacity(91000)==1);
    f.close(100000);assert(f.opacity(100000)==1);
    double offset=f.offset(130000);
    double alpha=f.opacity(130000);assert(alpha>0 && alpha<1);
    f.close(130000);assert(f.began==100000);
    f.open(130000);assert(std::abs(f.opacity(130000)-alpha)<1e-8);assert(std::abs(f.offset(130000)-offset)<1e-8); // quick reopen
    assert(!f.step(220000));assert(f.opacity(220000)==1);
    f.close(230000);assert(f.step(289999));assert(!f.step(290000));assert(f.opacity(290000)==0);
    smoothui::PopupFade quick;quick.open(1000);double y=quick.offset(31000);
    quick.close(31000);assert(std::abs(quick.offset(31000)-y)<1e-8);
    quick.open(41000);assert(std::abs(quick.offset(41000)-y)<1e-8);
    quick.step(131000);assert(quick.offset(131000)==0);
    std::cout<<"PASS: 90 ms open, 60 ms close, no typing replay, continuous quick reopen\n";
}
