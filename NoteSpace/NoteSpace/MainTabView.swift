//
//  MainTabView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct MainTabView: View {
    @EnvironmentObject private var dataManager: DataManager
    
    var body: some View {
        TabView {
            SpacesView()
                .tabItem {
                    Label("Spaces", systemImage: "rectangle.3.group")
                }
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
    }
}
