"use client";

import { SimulationSection } from "./Section/Simulation";
import { 
  Navbar, 
  NavBody, 
  NavItems, 
  MobileNav, 
  MobileNavHeader, 
  MobileNavMenu, 
  MobileNavToggle, 
  NavbarButton 
} from "@/components/ui/resizable-navbar";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function SimulationPage() {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  const navItems = [
    { name: "Home", link: "/" },
    { name: "Simulation", link: "/simulation" },
    { name: "About", link: "/about" },
  ];

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-black">
      <Navbar className="mt-0 top-0">
        <NavBody>
          <div className="relative z-20 flex items-center">
            <span className="text-xl font-bold text-black dark:text-white">Sim-Fluence</span>
          </div>
          <NavItems items={navItems} />
          <div className="relative z-20 flex flex-row items-center justify-end gap-2">
            <NavbarButton as="button" variant="secondary" onClick={() => router.push("/simulation")}>Login</NavbarButton>
            <NavbarButton as="button" onClick={() => router.push("/simulation")}>Get Started</NavbarButton>
          </div>
        </NavBody>
        <MobileNav>
          <MobileNavHeader>
            <div className="relative z-20 flex items-center">
              <span className="text-xl font-bold text-black dark:text-white">Sim-Fluence</span>
            </div>
            <MobileNavToggle isOpen={isOpen} onClick={() => setIsOpen(!isOpen)} />
          </MobileNavHeader>
          <MobileNavMenu isOpen={isOpen} onClose={() => setIsOpen(false)}>
            {navItems.map((item, idx) => (
              <NavbarButton
                key={idx}
                href={item.link}
                variant="secondary"
                className="w-full justify-start"
                onClick={() => setIsOpen(false)}
              >
                {item.name}
              </NavbarButton>
            ))}
            <NavbarButton as="button" variant="secondary" className="w-full justify-start" onClick={() => router.push("/simulation")}>Login</NavbarButton>
            <NavbarButton as="button" className="w-full justify-start" onClick={() => router.push("/simulation")}>Get Started</NavbarButton>
          </MobileNavMenu>
        </MobileNav>
      </Navbar>
      <SimulationSection />
    </main>
  );
}