const dummyData = {
  passes: [
    {
      passID: 1,
      timestamp: "2025-01-05T08:00:00",
      tagID: "TAG12345",
      tagProvider: "ProviderA",
      tollStation: "Station1",
      passType: "home",
      passCharge: 2.50,
    },
    {
      passID: 2,
      timestamp: "2025-01-05T09:30:00",
      tagID: "TAG67890",
      tagProvider: "ProviderB",
      tollStation: "Station2",
      passType: "visitor",
      passCharge: 3.00,
    },
    {
      passID: 3,
      timestamp: "2025-01-05T10:15:00",
      tagID: "TAG54321",
      tagProvider: "ProviderA",
      tollStation: "Station3",
      passType: "home",
      passCharge: 1.75,
    },
    {
      passID: 4,
      timestamp: "2025-01-06T11:00:00",
      tagID: "TAG11111",
      tagProvider: "ProviderC",
      tollStation: "Station4",
      passType: "business",
      passCharge: 4.50,
    },
    {
      passID: 5,
      timestamp: "2025-01-06T12:30:00",
      tagID: "TAG22222",
      tagProvider: "ProviderD",
      tollStation: "Station5",
      passType: "home",
      passCharge: 2.00,
    },
  ],

  costs: [
    {
      tollOpID: 1,
      tagOpID: 2,
      periodFrom: "2025-01-01",
      periodTo: "2025-01-05",
      nPasses: 10,
      passesCost: 25.75,
    },
    {
      tollOpID: 2,
      tagOpID: 1,
      periodFrom: "2025-01-01",
      periodTo: "2025-01-05",
      nPasses: 15,
      passesCost: 37.50,
    },
    {
      tollOpID: 3,
      tagOpID: 2,
      periodFrom: "2025-01-06",
      periodTo: "2025-01-06",
      nPasses: 12,
      passesCost: 28.00,
    },
    {
      tollOpID: 4,
      tagOpID: 3,
      periodFrom: "2025-01-06",
      periodTo: "2025-01-06",
      nPasses: 20,
      passesCost: 48.00,
    },
  ],

  stats: [
    {
      date: "2025-01-01",
      station: "Station1",
      totalPasses: 50,
      totalRevenue: 125.00,
    },
    {
      date: "2025-01-02",
      station: "Station2",
      totalPasses: 45,
      totalRevenue: 112.50,
    },
    {
      date: "2025-01-03",
      station: "Station3",
      totalPasses: 60,
      totalRevenue: 150.00,
    },
    {
      date: "2025-01-04",
      station: "Station4",
      totalPasses: 70,
      totalRevenue: 175.00,
    },
    {
      date: "2025-01-05",
      station: "Station5",
      totalPasses: 80,
      totalRevenue: 200.00,
    },
  ],
};

export default dummyData;
